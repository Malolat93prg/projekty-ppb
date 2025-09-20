import os, ssl, smtplib, pathlib
from email.message import EmailMessage

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "latest_report.md"

def send_email(subject: str, body: str, to_addr: str):
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT","587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    from_addr = os.getenv("SMTP_FROM", smtp_user)

    if not all([smtp_host, smtp_port, smtp_user, smtp_pass, to_addr]):
        print("Email pominięty — brak SMTP/EMAIL_TO.")
        return

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg.set_content(body)

    ctx = ssl.create_default_context()
    with smtplib.SMTP(smtp_host, smtp_port) as s:
        s.starttls(context=ctx)
        s.login(smtp_user, smtp_pass)
        s.send_message(msg)
        print("Wysłano e-mail do:", to_addr)

def main():
    to_addr = os.getenv("EMAIL_TO", "github93@wp.pl")
    if REPORT.exists():
        body = REPORT.read_text(encoding="utf-8")
    else:
        body = "Brak pliku raportu."

    send_email("PPB Auto-raport (GitHub Actions)", body, to_addr)

if __name__ == "__main__":
    main()
