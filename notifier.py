import json
import os
import smtplib
import datetime
import ecourt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

DATA_DIR = Path("data")
SNAPSHOT_FILE = DATA_DIR / "causelist_latest.json"
SUBSCRIBERS_FILE = DATA_DIR / "subscribers.json"

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_USER = os.environ.get("VC_EMAIL", "your@gmail.com")
SMTP_PASS = os.environ.get("VC_EMAIL_PASS", "your_app_password")

def fetch_cause_lists(date):
    court = ecourt.Court(state_code="1", court_code=None)
    ec = ecourt.ECourt(court)
    result = []
    for cl in ec.getCauseLists(date):
        result.append({
            "bench": cl.bench,
            "type": cl.type,
            "bench_id": cl.bench_id,
            "causelist_id": cl.causelist_id,
            "eliminated": cl.eliminated,
            "date": str(cl.date),
            "url": cl.url()
        })
    return result

def load_snapshot():
    if not SNAPSHOT_FILE.exists():
        return []
    with open(SNAPSHOT_FILE) as f:
        return json.load(f)

def save_snapshot(data):
    DATA_DIR.mkdir(exist_ok=True)
    with open(SNAPSHOT_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_subscribers():
    if not SUBSCRIBERS_FILE.exists():
        sample = [{"name": "Test User", "email": SMTP_USER, "watch": []}]
        DATA_DIR.mkdir(exist_ok=True)
        with open(SUBSCRIBERS_FILE, "w") as f:
            json.dump(sample, f, indent=2)
        print(f"Created sample subscribers file at {SUBSCRIBERS_FILE}")
        return sample
    with open(SUBSCRIBERS_FILE) as f:
        return json.load(f)

def diff_cause_lists(old, new):
    old_ids = {cl["bench_id"] + cl["causelist_id"] for cl in old}
    added   = [cl for cl in new if cl["bench_id"] + cl["causelist_id"] not in old_ids]
    new_ids = {cl["bench_id"] + cl["causelist_id"] for cl in new}
    removed = [cl for cl in old if cl["bench_id"] + cl["causelist_id"] not in new_ids]
    return {"added": added, "removed": removed, "all": new}

def matches_watch(cl, watch):
    if not watch:
        return True
    return any(w.upper() in cl["bench"].upper() for w in watch)

def build_email_html(subscriber, added, removed, all_cls):
    date_str = datetime.date.today().strftime("%d %B %Y")
    name  = subscriber["name"]
    watch = subscriber.get("watch", [])
    my_added   = [cl for cl in added   if matches_watch(cl, watch)]
    my_removed = [cl for cl in removed if matches_watch(cl, watch)]
    my_all     = [cl for cl in all_cls if matches_watch(cl, watch) and not cl["eliminated"]]
    if not my_all and not my_added and not my_removed:
        return None

    def rows(cls, bg=""):
        s = ""
        for cl in cls:
            status = "ELIMINATED" if cl["eliminated"] else cl["type"]
            style = f"background:{bg};" if bg else ""
            s += f"<tr style='{style}'><td style='padding:6px 10px;'>{cl['bench']}</td><td style='padding:6px 10px;'>{status}</td><td style='padding:6px 10px;'><a href='{cl['url']}'>View</a></td></tr>"
        return s

    new_sec = f"<h3 style='color:#1a7f37;'>New Listings ({len(my_added)})</h3><table border='1' cellspacing='0' style='border-collapse:collapse;width:100%;'><tr style='background:#f0f0f0;'><th>Bench</th><th>Type</th><th>Link</th></tr>{rows(my_added,'#e6f4ea')}</table>" if my_added else ""
    rem_sec = f"<h3 style='color:#c62828;'>Removed ({len(my_removed)})</h3><table border='1' cellspacing='0' style='border-collapse:collapse;width:100%;'><tr style='background:#f0f0f0;'><th>Bench</th><th>Type</th><th>Link</th></tr>{rows(my_removed,'#fce8e6')}</table>" if my_removed else ""
    watch_label = ", ".join(watch) if watch else "All benches"

    return f"""<html><body style='font-family:Arial,sans-serif;font-size:14px;max-width:800px;margin:auto;'>
<h2>Bombay HC Cause List - {date_str}</h2>
<p>Dear {name},</p><p>Watching: <em>{watch_label}</em></p>
{new_sec}{rem_sec}
<h3>Full Cause List Today ({len(my_all)} benches)</h3>
<table border='1' cellspacing='0' style='border-collapse:collapse;width:100%;'>
<tr style='background:#f0f0f0;'><th>Bench</th><th>Type</th><th>Link</th></tr>
{rows(my_all)}
</table>
<p style='color:#888;font-size:12px;margin-top:20px;'>Sent by Virtual Clerk</p>
</body></html>"""

def send_email(to_name, to_email, subject, html_body):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = f"Virtual Clerk <{SMTP_USER}>"
    msg["To"]      = f"{to_name} <{to_email}>"
    msg.attach(MIMEText(html_body, "html"))
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
    print(f"  Sent to {to_name} <{to_email}>")

def main():
    today = datetime.date.today()
    print(f"Virtual Clerk starting - {today}")
    print("Fetching Bombay HC cause lists...")
    current = fetch_cause_lists(today)
    print(f"  Got {len(current)} cause lists")
    previous = load_snapshot()
    diff = diff_cause_lists(previous, current)
    print(f"  Added: {len(diff['added'])}, Removed: {len(diff['removed'])}")
    save_snapshot(current)
    subscribers = load_subscribers()
    print(f"Notifying {len(subscribers)} subscriber(s)...")
    date_str = today.strftime("%d %B %Y")
    sent = 0
    for sub in subscribers:
        html = build_email_html(sub, diff["added"], diff["removed"], diff["all"])
        if html is None:
            print(f"  Nothing relevant for {sub['name']}, skipping")
            continue
        subject = f"Bombay HC Cause List - {date_str}"
        if diff["added"]:
            subject = f"{len(diff['added'])} new listing(s) - Bombay HC - {date_str}"
        try:
            send_email(sub["name"], sub["email"], subject, html)
            sent += 1
        except Exception as e:
            print(f"  Failed to send to {sub['email']}: {e}")
    print(f"\nDone. Sent {sent}/{len(subscribers)} emails.")

if __name__ == "__main__":
    main()
