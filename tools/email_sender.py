import os, ssl, smtplib
from email.message import EmailMessage
from datetime import datetime
from zoneinfo import ZoneInfo

REPORT_PATH = "reports/latest_report.md"

def main():
    with open(REPORT_PATH, "r", encoding="utf-8") as f:
        body = f.read()

    now_pl = datetime.now(ZoneInfo(os.environ.get("TZ", "Europe/Warsaw")))
    subject = f"[PPB] Raport godzinny – {now_pl.strftime('%Y-%m-%d %H:%M')}"

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"]    = os.environ["MAIL_FROM"]
    msg["To"]      = os.environ["MAIL_TO"]
    msg.set_content(body)

    host = os.environ["SMTP_HOST"]
    port = int(os.environ.get("SMTP_PORT", "465"))
    user = os.environ["SMTP_USER"]
    pwd  = os.environ["SMTP_PASS"]

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(host, port, context=context) as smtp:
        smtp.login(user, pwd)
        smtp.send_message(msg)
    print("Email sent OK")

if __name__ == "__main__":
    main()
