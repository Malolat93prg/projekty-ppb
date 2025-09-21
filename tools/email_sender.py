import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.utils import formatdate
from datetime import datetime
try:
    from zoneinfo import ZoneInfo  # py3.9+
except Exception:
    ZoneInfo = None

def env(name, required=True, default=None):
    val = os.environ.get(name, default)
    if required and (val is None or str(val).strip() == ""):
        raise RuntimeError(f"Missing required secret/var: {name}")
    return val

def now_pl(tz_name):
    if ZoneInfo:
        return datetime.now(ZoneInfo(tz_name))
    return datetime.now()

def main():
    host = env("SMTP_HOST")
    port = int(env("SMTP_PORT"))
    user = env("SMTP_USER")
    password = env("SMTP_PASS")
    mail_from = env("MAIL_FROM")
    mail_to = env("MAIL_TO")
    tz = env("TZ", default="Europe/Warsaw")

    # Wczytaj raport z pliku (tworzony wcześniej przez generate_report.py)
    report_path = "reports/latest_report.md"
    if not os.path.exists(report_path):
        body = "Brak pliku raportu (reports/latest_report.md)."
    else:
        with open(report_path, "r", encoding="utf-8") as f:
            body = f.read()

    now = now_pl(tz)
    subject = f"[PPB] Raport godzinowy – {now.strftime('%Y-%m-%d %H:%M')} ({tz})"

    msg = MIMEText(body, _charset="utf-8")
    msg["Subject"] = subject
    msg["From"] = mail_from
    msg["To"] = mail_to
    msg["Date"] = formatdate(localtime=True)

    context = ssl.create_default_context()

    # Autodetekcja trybu:
    if port == 465:
        # SSL od razu
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
        raise RuntimeError(f"Unsupported SMTP_PORT: {port} (use 465 for SSL or 587 for STARTTLS)")

if __name__ == "__main__":
    try:
        main()
        print("Email sent OK.")
    except Exception as e:
        # Czytelny log w Actions zamiast niejasnego tracebacka
        import traceback
        print("ERROR sending email:", e)
        traceback.print_exc()
        raise
