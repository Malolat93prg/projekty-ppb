from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
OUT = Path("reports/daily"); OUT.mkdir(parents=True, exist_ok=True)
ts = datetime.now(ZoneInfo("Europe/Warsaw")).strftime("%Y-%m-%d %H:%M")
fname = OUT / ("PPB_daily_" + datetime.now(ZoneInfo("Europe/Warsaw")).strftime("%Y-%m-%d") + ".md")
fname.write_text(f"# PPB – Raport dzienny\n**Czas (Europe/Warsaw):** {ts}\n", encoding="utf-8")
print("[daily] wrote", fname)
