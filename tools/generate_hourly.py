from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
OUT = Path("reports/hourly"); OUT.mkdir(parents=True, exist_ok=True)
ts = datetime.now(ZoneInfo("Europe/Warsaw")).strftime("%Y-%m-%d %H:%M")
fname = OUT / ("PPB_hourly_" + datetime.now(ZoneInfo("Europe/Warsaw")).strftime("%Y-%m-%d_%H") + ".md")
fname.write_text(f"# PPB – Raport godzinowy\n**Czas (Europe/Warsaw):** {ts}\n", encoding="utf-8")
print("[hourly] wrote", fname)
