import smtplib
from email.mime.text import MIMEText
from tomorrow_digest import build_digest, tomorrow_cases

EMAIL = "yourgmail@gmail.com"
PASSWORD = "app-password"

def send():

    cases = tomorrow_cases()

    if not cases:
        print("No matters tomorrow")
        return

    body = build_digest(cases)

    msg = MIMEText(body)

    msg["Subject"] = "Tomorrow's Matters"
    msg["From"] = EMAIL
    msg["To"] = EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com",465) as s:
        s.login(EMAIL,PASSWORD)
        s.send_message(msg)

    print("Digest sent")

if __name__ == "__main__":
    send()

