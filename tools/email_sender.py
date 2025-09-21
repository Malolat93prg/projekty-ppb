# tools/email_sender_attach.py
# Wysyłka raportu e-mailem z ZAŁĄCZNIKAMI (Gmail / SSL 465 lub STARTTLS 587)
# Wymagane sekrety: SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, MAIL_FROM, MAIL_TO, TZ

import os
import smtplib
import ssl
import mimetypes
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from email import encoders
from pathlib import Path
from datetime import datetime
import shutil

try:
    from zoneinfo import ZoneInfo  # Python >= 3.9
except Exception:
    ZoneInfo = None

REPO_ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = REPO_ROOT / "reports"

def env(name: str, required: bool = True, default: str | None = None) -> str:
    val = os.environ.get(name, default)
    if required and (val is None or str(val).strip() == ""):
        raise RuntimeError(f"Missing required secret/var: {name}")
    return val

def now_tz(tz_name: str) -> datetime:
    if ZoneInfo:
        return datetime.now(ZoneInfo(tz_name))
    return datetime.now()

def guess_latest_archive_name() -> str:
    # wybierz najnowszy report-YYYY-MM-DD_HHMM.md na podstawie mtime
    md_files = sorted(REPORTS_DIR.glob("report-*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    if md_files:
        stem = md_files[0].stem  # "report-YYYY-MM-DD_HHMM"
        return stem
    return None

def attach_file(msg: MIMEMultipart, path: Path):
    if not path or not path.exists():
        return
    ctype, encoding = mimetypes.guess_type(str(path))
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"
    maintype, subtype = ctype.split("/", 1)

    with open(path, "rb") as f:
        part = MIMEBase(maintype, subtype)
        part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f'attachment; filename="{path.name}"')
    msg.attach(part)

def main():
    host = env("SMTP_HOST")
    port = int(env("SMTP_PORT"))
    user = env("SMTP_USER")
    password = env("SMTP_PASS")
    mail_from = env("MAIL_FROM")
    mail_to = env("MAIL_TO")
    tz = env("TZ", default="Europe/Warsaw")

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    # Treść do maila
    latest_md = REPORTS_DIR / "latest_report.md"
    if latest_md.exists():
        body = latest_md.read_text(encoding="utf-8")
    else:
        body = "Brak pliku raportu (reports/latest_report.md). Upewnij się, że tools/generate_report.py został uruchomiony wcześniej."

    now = now_tz(tz)
    subject = f"[PPB] Raport — {now.strftime('%Y-%m-%d %H:%M')} ({tz}) + załączniki"

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = mail_from
    msg["To"] = mail_to
    msg["Date"] = formatdate(localtime=True)

    # Część tekstowa (treść maila)
    msg.attach(MIMEText(body, _charset="utf-8"))

    # Ustal najnowszy archiwalny raport i przygotuj ZIP
    stem = guess_latest_archive_name()  # np. "report-2025-09-21_1930"
    archive_zip = None
    if stem:
        arch_md = REPORTS_DIR / f"{stem}.md"
        # dołącz latest_report.md i archiwalny
        attach_file(msg, latest_md)
        attach_file(msg, arch_md)
        # ZIP
        # przygotuj tymczasowy katalog do spakowania
        tmp_dir = REPORTS_DIR / f"{stem}-tmp"
        try:
            tmp_dir.mkdir(exist_ok=True)
            # skopiuj oba pliki (jeśli istnieją)
            if latest_md.exists():
                (tmp_dir / latest_md.name).write_text(latest_md.read_text(encoding="utf-8"), encoding="utf-8")
            if arch_md.exists():
                (tmp_dir / arch_md.name).write_text(arch_md.read_text(encoding="utf-8"), encoding="utf-8")
            # utwórz zip
            archive_zip = REPORTS_DIR / f"{stem}.zip"
            shutil.make_archive(str(archive_zip.with_suffix("")), "zip", tmp_dir)
            # dołącz ZIP
            attach_file(msg, archive_zip)
        finally:
            # posprzątaj tymczasowy katalog
            if tmp_dir.exists():
                shutil.rmtree(tmp_dir, ignore_errors=True)
    else:
        # brak archiwalnych plików – dołącz tylko latest (jeśli jest)
        attach_file(msg, latest_md)

    # Wysyłka (SSL 465 lub STARTTLS 587)
    context = ssl.create_default_context()
    if port == 465:
        with smtplib.SMTP_SSL(host, port, context=context) as smtp:
            smtp.login(user, password)
            smtp.sendmail(mail_from, [mail_to], msg.as_string())
    elif port == 587:
        with smtplib.SMTP(host, port, timeout=30) as smtp:
            smtp.ehlo()
            smtp.starttls(context=context)
            smtp.ehlo()
            smtp.login(user, password)
            smtp.sendmail(mail_from, [mail_to], msg.as_string())
    else:
        raise RuntimeError(f"Unsupported SMTP_PORT: {port} (use 465 or 587)")

    print("Email with attachments sent OK.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        print("ERROR sending email with attachments:", e)
        traceback.print_exc()
        raise
