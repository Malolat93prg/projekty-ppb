from __future__ import annotations
import os, glob, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from zoneinfo import ZoneInfo

def env(name: str, default: str | None = None, required: bool = True) -> str:
    val = os.environ.get(name, default)
    if required and (val is None or str(val).strip() == ""):
        raise RuntimeError(f"Missing required secret/var: {name}")
    return val

def latest_weekly_md() -> str:
    files = sorted(glob.glob("reports/*-weekly-summary.md"))
    if not files:
        raise FileNotFoundError("No weekly summary found in reports/*.md")
    return files[-1]

def main():
    tz_name = os.environ.get("TZ", "Europe/Warsaw")
    tz = ZoneInfo(tz_name)
    now = datetime.now(tz)

    host = env("SMTP_HOST")
    port = int(env("SMTP_PORT"))
    user = env("SMTP_USER")
    passwd = env("SMTP_PASS")
    mail_from = env("MAIL_FROM")
    mail_to = env("MAIL_TO")

    md_path = latest_weekly_md()

    subject = f"PPB — Weekly Summary ({now:%Y-%m-%d %H:%M %Z})"
    body_text = f"""Cześć,

W załączniku tygodniowe podsumowanie projektu.
Godzina lokalna: {now:%Y-%m-%d %H:%M %Z}

Pozdrawiam,
PPB Bot
"""

    msg = MIMEMultipart()
    msg["From"] = mail_from
    msg["To"] = mail_to
    msg["Subject"] = subject
    msg.attach(MIMEText(body_text, "plain", "utf-8"))

    with open(md_path, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f'attachment; filename="{os.path.basename(md_path)}"')
    msg.attach(part)

    with smtplib.SMTP_SSL(host, port) as smtp:
        smtp.login(user, passwd)
        smtp.sendmail(mail_from, [a.strip() for a in mail_to.split(",") if a.strip()], msg.as_string())

    print(f"[OK] Sent weekly email with attachment: {md_path}")

if __name__ == "__main__":
    main()