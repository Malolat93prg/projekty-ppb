# PPB — SMTP sender for weekly summary
import os, smtplib, ssl
from email.message import EmailMessage
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
latest_path_file = ROOT / "reports" / "weekly" / "_latest_path.txt"
if not latest_path_file.exists():
    raise SystemExit("Brak pliku z najnowszym podsumowaniem ( _latest_path.txt ).")

md_path = Path(latest_path_file.read_text(encoding="utf-8").strip())
if not md_path.exists():
    raise SystemExit(f"Nie znaleziono pliku raportu: {md_path}")

smtp_host = os.environ.get("SMTP_HOST")
smtp_port = int(os.environ.get("SMTP_PORT", "587"))
smtp_user = os.environ.get("SMTP_USER")
smtp_pass = os.environ.get("SMTP_PASS")
mail_to   = os.environ.get("MAIL_TO")
mail_from = os.environ.get("MAIL_FROM", smtp_user)

if not all([smtp_host, smtp_port, smtp_user, smtp_pass, mail_to, mail_from]):
    raise SystemExit("Brakuje zmiennych środowiskowych SMTP_HOST/SMTP_PORT/SMTP_USER/SMTP_PASS/MAIL_TO/MAIL_FROM")

body = md_path.read_text(encoding="utf-8", errors="ignore")

msg = EmailMessage()
msg["Subject"] = f"PPB — Tygodniowe podsumowanie: {md_path.stem}"
msg["From"] = mail_from
msg["To"] = mail_to
msg.set_content("W załączeniu treść tygodniowego raportu (markdown w treści e-maila).")
msg.add_alternative(f"<pre style='font-family:monospace'>{body}</pre>", subtype="html")

with open(md_path, "rb") as f:
    data = f.read()
msg.add_attachment(data, maintype="text", subtype="markdown", filename=md_path.name)

context = ssl.create_default_context()
with smtplib.SMTP(smtp_host, smtp_port) as server:
    server.starttls(context=context)
    server.login(smtp_user, smtp_pass)
    server.send_message(msg)

print("[OK] Wysłano e-mail z tygodniowym podsumowaniem do:", mail_to)
