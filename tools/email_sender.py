
import os, smtplib, ssl
from email.mime.text import MIMEText
from zoneinfo import ZoneInfo
from datetime import datetime

def env(name, default=None, require=False):
    v = os.environ.get(name, default)
    if require and not v:
        raise RuntimeError(f"Missing required secret/var: {name}")
    return v

def load_body():
    # prefer daily report
    candidates = ["reports/latest_daily.md", "reports/daily/latest.md", "reports/latest_hourly.md"]
    for c in candidates:
        if os.path.exists(c):
            with open(c, "r", encoding="utf-8") as f:
                return f.read()
    return "Brak treści raportu – spróbuj ponownie później."

def main():
    host = env("SMTP_HOST", require=True)
    port = int(env("SMTP_PORT", "465"))
    user = env("SMTP_USER", require=True)
    password = env("SMTP_PASS", require=True)
    mail_from = env("MAIL_FROM", require=True)
    mail_to = env("MAIL_TO", require=True)
    tz = ZoneInfo(os.environ.get("TZ","Europe/Warsaw"))
    now = datetime.now(tz)
    subject = f"PPB – Raport dzienny ({now.strftime('%Y-%m-%d %H:%M %Z')})"
    body = load_body()
    msg = MIMEText(body, _charset="utf-8")
    msg["Subject"] = subject
    msg["From"] = mail_from
    msg["To"] = mail_to
    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL(host, port, context=ctx) as smtp:
        smtp.login(user, password)
        smtp.sendmail(mail_from, [mail_to], msg.as_string())
    print("E-mail sent")

if __name__ == "__main__":
    main()
