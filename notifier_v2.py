import os, re, json, smtplib, datetime, subprocess, tempfile
import requests
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
import cv2, numpy as np

BASE      = "https://hcservices.ecourts.gov.in/ecourtindiaHC/"
DATA      = Path("data")
SUBS_F    = DATA / "subscribers.json"
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_USER = os.environ.get("VC_EMAIL", "")
SMTP_PASS = os.environ.get("VC_EMAIL_PASS", "")
UA        = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"}

def solve_captcha(session):
    for _ in range(15):
        cr = session.get(BASE + "securimage/securimage_show.php", headers=UA)
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False, dir='.') as f:
            f.write(cr.content); fname = f.name
        src = cv2.imread(fname)
        if src is None: continue
        _, thr = cv2.threshold(src, 102, 255, cv2.THRESH_BINARY)
        mask = cv2.inRange(src, np.array([0x70,0x70,0x70],dtype=np.uint8), np.array([0x70,0x70,0x70],dtype=np.uint8))
        masked = cv2.dilate(cv2.bitwise_and(src,src,mask=mask), cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)))
        dst = cv2.inpaint(thr, cv2.cvtColor(masked,cv2.COLOR_BGR2GRAY), 7, cv2.INPAINT_NS)
        dst = cv2.GaussianBlur(cv2.dilate(dst, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))),(5,5),0)
        dst = cv2.bilateralFilter(dst,5,75,75)
        _,dst = cv2.threshold(cv2.cvtColor(dst,cv2.COLOR_BGR2GRAY),0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        dst = dst[15:65,27:190]
        cv2.imwrite("cap.png", dst)
        p = subprocess.Popen(["tesseract","cap.png","stdout","--oem","1","--psm","8",
            "-c","tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz0123456789"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        result = p.communicate()[0].decode().strip()
        if len(result) == 5: return result
    return None


def get_case_detail(session, case_no, cino, court_code, token):
    """Fetch next hearing date and bench for a case."""
    try:
        r = session.post(BASE+"cases/o_civil_case_history.php",
            data={"court_code":court_code,"state_code":"1","dist_code":"1",
                  "case_no":case_no,"cino":cino,"token":token,"appFlag":""},
            headers={**UA,
                "Referer":BASE+"cases/qs_civil_advocate.php?state_cd=1&dist_cd=1&court_code=1&stateNm=",
                "X-Requested-With":"XMLHttpRequest"}, timeout=10)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.text, 'html.parser')
        for table in soup.find_all('table'):
            headers = [th.get_text(strip=True) for th in table.find_all('th')]
            if 'Hearing Date' in headers:
                rows = table.find_all('tr')
                # Last row with a hearing date = most recent/next
                last = None
                for row in rows[1:]:
                    cols = [td.get_text(strip=True) for td in row.find_all('td')]
                    if len(cols) >= 4 and cols[3]:
                        last = cols
                if last:
                    return {"next_date": last[3], "bench": last[1], "purpose": last[4] if len(last)>4 else ""}
    except Exception as e:
        pass
    return {}

def parse_cases(raw):
    raw = raw.replace("&amp;","&").replace("&nbsp;"," ").replace('\ufeff','')
    raw = re.sub(r'<br\s*/?>', '|', raw)
    blocks = raw.split('##')
    cases = []
    for block in blocks[1:]:
        block = block.strip().strip('~')
        if not block: continue
        parts = block.split('~')
        if len(parts) < 7: continue
        case_no = parts[1].strip()
        party_raw = parts[2].replace('\n',' ')
        if '|Versus|' in party_raw:
            pet, resp = party_raw.split('|Versus|', 1)
        else:
            pet, resp = party_raw, ''
        cnr      = parts[3].strip()
        court    = parts[6].strip() if len(parts) > 6 else ''
        adv_raw  = parts[7].strip() if len(parts) > 7 else ''
        advocates = [a.strip().replace('\n',' ') for a in adv_raw.split('|') if a.strip()]
        if case_no:
            cases.append({"case_no": case_no, "petitioner": pet.strip(),
                          "respondent": resp.strip(), "cnr": cnr,
                          "court": court, "advocates": advocates,
                          "_internal": parts[0].strip(),
                          "_court_code": parts[4].strip() if len(parts)>4 else "1",
                          "_token": parts[9].strip() if len(parts)>9 else ""})
    return cases

def search_advocate(name, date_dmy):
    for attempt in range(5):
        session = requests.Session()
        r = session.get(BASE+"cases/qs_civil_advocate.php?state_cd=1&dist_cd=1&court_code=1&stateNm=", headers=UA)
        csrf = BeautifulSoup(r.text,'html.parser').find('input',{'name':'__csrf_magic'})['value']
        captcha = solve_captcha(session)
        if not captcha: continue
        print(f"  Attempt {attempt+1} captcha: {captcha}")
        r2 = session.post(BASE+"cases/qs_civil_advocate_qry.php",
            data={"action_code":"showRecords","state_code":"1","dist_code":"1",
                  "court_code":"1","advocate_name":name,"search_type":"1",
                  "f":"Pending","caselist_date":date_dmy,"captcha":captcha,"__csrf_magic":csrf},
            headers={**UA,"Referer":BASE+"cases/qs_civil_advocate.php?state_cd=1&dist_cd=1&court_code=1&stateNm=",
                     "X-Requested-With":"XMLHttpRequest"})
        print(f"  Response size: {len(r2.text)}, content: {r2.text[:30]}")
        if len(r2.text) > 20:
            return parse_cases(r2.text)
    return []

def search_party(name):
    session = requests.Session()
    r = session.get(BASE+"cases/ki_petres.php?state_cd=1&dist_cd=1&court_code=1&stateNm=", headers=UA)
    csrf = BeautifulSoup(r.text,'html.parser').find('input',{'name':'__csrf_magic'})['value']
    captcha = solve_captcha(session)
    if not captcha: return []
    print(f"  Captcha: {captcha}")
    r2 = session.post(BASE+"cases/ki_petres.php?state_cd=1&dist_cd=1&court_code=1&stateNm=",
        data={"action_code":"showRecords","state_code":"1","dist_code":"1",
              "court_code":"1","petres_name":name,"f":"Pending",
              "captcha":captcha,"__csrf_magic":csrf},
        headers={**UA,"Referer":BASE+"cases/ki_petres.php?state_cd=1&dist_cd=1&court_code=1&stateNm=",
                 "X-Requested-With":"XMLHttpRequest"})
    print(f"  Response size: {len(r2.text)}")
    if len(r2.text) < 20: return []
    cases = parse_cases(r2.text)
    print(f"  Fetching next dates for {min(len(cases),50)} cases...")
    for c in cases[:50]:
        detail = get_case_detail(session, c["_internal"], c["cnr"], c["_court_code"], c["_token"])
        c.update(detail)
    return cases

def build_email(sub, cases, date_str):
    rows = ""
    for c in cases:
        advocates = ", ".join(c["advocates"]) if c["advocates"] else "-"
        next_date = c.get("next_date","—")
        bench     = c.get("bench","—")
        purpose   = c.get("purpose","")
        rows += f"""<tr>
          <td style='padding:6px 10px;font-weight:bold;color:#1a237e;'>{c['case_no']}</td>
          <td style='padding:6px 10px;'>{c['petitioner'][:50]}</td>
          <td style='padding:6px 10px;'>{c['respondent'][:50]}</td>
          <td style='padding:6px 10px;font-size:12px;background:#e8f5e9;font-weight:bold;'>{next_date}</td>
          <td style='padding:6px 10px;font-size:11px;'>{bench[:50]}</td>
          <td style='padding:6px 10px;font-size:11px;color:#555;'>{purpose}</td>
        </tr>"""
    return f"""<html><body style='font-family:Arial,sans-serif;font-size:14px;max-width:950px;margin:auto;'>
    <h2 style='color:#1a237e;'>⚖️ Bombay HC — Your Listed Cases · {date_str}</h2>
    <p>Dear <strong>{sub['name']}</strong>,</p>
    <p><strong>{len(cases)} case(s)</strong> matching your watch are listed today.</p>
    <table border='1' cellspacing='0' style='border-collapse:collapse;width:100%;font-size:13px;'>
      <tr style='background:#1a237e;color:white;text-align:left;'>
        <th style='padding:8px;'>Case No</th><th style='padding:8px;'>Petitioner</th>
        <th style='padding:8px;'>Respondent</th><th style='padding:8px;'>Next Date</th>
        <th style='padding:8px;'>Bench</th><th style='padding:8px;'>Purpose</th>
      </tr>{rows}
    </table>
    <p style='margin-top:16px;'>
      <a href='https://hcservices.ecourts.gov.in/ecourtindiaHC/index_highcourt.php?state_cd=1&dist_cd=1'
         style='background:#1a237e;color:white;padding:8px 16px;text-decoration:none;border-radius:4px;'>
        Open Bombay HC Portal
      </a>
    </p>
    <p style='color:#888;font-size:11px;margin-top:20px;'>Sent by Virtual Clerk · {date_str}</p>
    </body></html>"""

def send_email(to_name, to_email, subject, html):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = f"Virtual Clerk <{SMTP_USER}>"
    msg["To"]      = f"{to_name} <{to_email}>"
    msg.attach(MIMEText(html, "html"))
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as s:
        s.login(SMTP_USER, SMTP_PASS)
        s.send_message(msg)
    print(f"  Email sent to {to_name} <{to_email}>")

def load_subscribers():
    if not SUBS_F.exists():
        sample = [{"name":"Test Advocate","email":SMTP_USER,
                   "advocate_name":"SHARMA","client_names":[]}]
        DATA.mkdir(exist_ok=True)
        SUBS_F.write_text(json.dumps(sample, indent=2))
    return json.loads(SUBS_F.read_text())

def main():
    today    = datetime.date.today()
    date_str = today.strftime("%d %B %Y")
    date_dmy = today.strftime("%d-%m-%Y")
    print(f"Virtual Clerk v2 — {date_str}")

    for sub in load_subscribers():
        print(f"\nProcessing: {sub['name']}")
        all_cases = []

        if sub.get("advocate_name"):
            print(f"  Searching advocate: {sub['advocate_name']}")
            found = search_advocate(sub["advocate_name"], date_dmy)
            print(f"  Found {len(found)} cases")
            all_cases.extend(found)

        for client in sub.get("client_names", []):
            print(f"  Searching party: {client}")
            found = search_party(client)
            print(f"  Found {len(found)} cases")
            all_cases.extend(found)

        seen, unique = set(), []
        for c in all_cases:
            if c["case_no"] not in seen:
                seen.add(c["case_no"]); unique.append(c)

        print(f"  Total unique cases: {len(unique)}")
        if not unique:
            print("  No cases, skipping email"); continue

        DATA.mkdir(exist_ok=True)
        (DATA / f"cases_{today}.json").write_text(json.dumps(unique, indent=2))

        html    = build_email(sub, unique[:50], date_str)
        subject = f"⚖️ {len(unique)} case(s) listed today · Bombay HC · {date_str}"
        try:
            send_email(sub["name"], sub["email"], subject, html)
        except Exception as e:
            print(f"  Email failed: {e}")

    print("\nDone.")

if __name__ == "__main__":
    main()
