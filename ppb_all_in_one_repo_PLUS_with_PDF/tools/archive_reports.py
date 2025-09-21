# Zip the entire reports/ folder into archives/YYYY-MM-DD_reports.zip
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import zipfile, os

ROOT = Path(__file__).resolve().parents[1]
TZ = ZoneInfo("Europe/Warsaw")
now = datetime.now(TZ)
zip_name = ROOT / "archives" / f"{now.strftime('%Y-%m-%d')}_reports.zip"

with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as z:
    for p in (ROOT/"reports").rglob("*"):
        if p.is_file():
            z.write(p, p.relative_to(ROOT))

print("[OK] Utworzono archiwum:", zip_name)
