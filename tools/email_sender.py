import os, smtplib, ssl
from email.mime.text import MIMEText
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path

def load_latest(path: Path) -> str:
    files = sorted(path.glob("*.md"))
    if not files:
        return "Brak raportu do wysyłki."
    return files[-1].read_text(encoding="utf-8")

def main():
    mode = os.environ.get("MODE","daily")
    if mode == "weekly":
        folder = Path("reports/weekly")
        subj = "PPB – Raport tygodniowy"
    else:
        folder = Path("reports/daily")
        subj = "PPB – Raport dzienny"

    body = load_latest(folder)

    host = os.environ["SMTP_HOST"]
    port = int(os.environ.get("SMTP_PORT","587"))
    user = os.environ["SMTP_USER"]
    pwd  = os.environ["SMTP_PASS"]
    mail_from = os.environ["MAIL_FROM"]
    mail_to   = os.environ["MAIL_TO"]

    msg = MIMEText(body, "plain", "utf-8")
    ts = datetime.now(ZoneInfo("Europe/Warsaw")).strftime("%Y-%m-%d %H:%M")
    msg["Subject"] = f"{subj} – {ts}"
    msg["From"] = mail_from
    msg["To"] = mail_to

    ctx = ssl.create_default_context()
    with smtplib.SMTP(host, port) as server:
        server.starttls(context=ctx)
        server.login(user, pwd)
        server.sendmail(mail_from, [mail_to], msg.as_string())
    print("Email sent to", mail_to)

if __name__ == "__main__":
    main()
