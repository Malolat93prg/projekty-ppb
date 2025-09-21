# tools/email_sender.py
# Wysyłka raportu e-mailem (dla Gmaila)
# Obsługuje SSL (465) i STARTTLS (587)
# Wymagane sekrety w GitHub Actions:
# SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, MAIL_FROM, MAIL_TO, TZ

import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.utils import formatdate
from datetime import datetime
try:
    from zoneinfo import ZoneInfo  # Python >=3.9
except Exception:
    ZoneInfo = None


def env(name: str, required: bool = True, default: str | None = None) -> str:
    val = os.environ.get(name, default)
    if required and (val is None or str(val).strip() == ""):
        raise RuntimeError(f"Missing required secret/var: {name}")
    return val


def now_tz(tz_name: str) -> datetime:
    if ZoneInfo:
        return datetime.now(ZoneInfo(tz_name))
    return datetime.now()


def main() -> None:
    host = env("SMTP_HOST")
    port = int(env("SMTP_PORT"))
    user = env("SMTP_USER")
    password = env("SMTP_PASS")
    mail_from = env("MAIL_FROM")
    mail_to = env("MAIL_TO")
    tz = env("TZ", default="Europe/Warsaw")

    # Wczytaj treść raportu (generowanego wcześniej w workflow)
    report_path = "reports/latest_report.md"
    if not os.path.exists(report_path):
        body = "Brak pliku raportu (reports/latest_report.md)."
    else:
        with open(report_path, "r", encoding="utf-8") as f:
            body = f.read()

    now = now_tz(tz)
    subject = f"[PPB] Raport godzinowy – {now.strftime('%Y-%m-%d %H:%M')} ({tz})"

    msg = MIMEText(body, _charset="utf-8")
    msg["Subject"] = subject
    msg["From"] = mail_from
    msg["To"] = mail_to
    msg["Date"] = formatdate(localtime=True)

    context = ssl.create_default_context()

    if port == 465:
        # SSL (najczęściej dla Gmaila)
        with smtplib.SMTP_SSL(host, port, context=context) as smtp:
            smtp.login(user, password)
            smtp.sendmail(mail_from, [mail_to], msg.as_string())
    elif port == 587:
        # STARTTLS
        with smtplib.SMTP(host, port, timeout=30) as smtp:
            smtp.ehlo()
            smtp.starttls(context=context)
            smtp.ehlo()
            smtp.login(user, password)
            smtp.sendmail(mail_from, [mail_to], msg.as_string())
    else:
        raise RuntimeError(
            f"Unsupported SMTP_PORT: {port} (use 465 for SSL or 587 for STARTTLS)"
        )

    print("Email sent OK.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        print("ERROR sending email:", e)
        traceback.print_exc()
        raise
