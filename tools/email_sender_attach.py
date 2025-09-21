import smtplib, ssl, os
from email.message import EmailMessage
from datetime import datetime

def env(name, default=None):
    value = os.getenv(name, default)
    if not value:
        raise RuntimeError(f"Missing required secret/var: {name}")
    return value

def main():
    smtp_host = env("SMTP_HOST")
    smtp_port = int(env("SMTP_PORT", "465"))
    smtp_user = env("SMTP_USER")
    smtp_pass = env("SMTP_PASS")
    mail_from = env("MAIL_FROM")
    mail_to = env("MAIL_TO")

    msg = EmailMessage()
    msg["Subject"] = f"📊 Daily Report PPB – {datetime.now().strftime('%Y-%m-%d')}"
    msg["From"] = mail_from
    msg["To"] = mail_to
    msg.set_content("W załączniku znajduje się dzienny raport i paczka ZIP 📎")

    # dołącz plik raportu
    report_path = "reports/latest_report.md"
    if os.path.exists(report_path):
        with open(report_path, "rb") as f:
            msg.add_attachment(f.read(), maintype="text", subtype="markdown", filename="latest_report.md")

    # dołącz ZIP (jeśli istnieje)
    zip_path = "reports/daily_bundle.zip"
    if os.path.exists(zip_path):
        with open(zip_path, "rb") as f:
            msg.add_attachment(f.read(), maintype="application", subtype="zip", filename="daily_bundle.zip")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context) as smtp:
        smtp.login(smtp_user, smtp_pass)
        smtp.send_message(msg)

if __name__ == "__main__":
    main()
