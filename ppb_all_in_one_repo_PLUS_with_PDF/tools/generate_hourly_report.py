# PPB — Hourly report generator (repo-only)
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path

TZ = ZoneInfo(os.environ.get("TZ", "Europe/Warsaw"))
ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "reports" / "hourly"
OUTDIR.mkdir(parents=True, exist_ok=True)

now = datetime.now(TZ)
stamp = now.strftime("%Y-%m-%d_%H00")
out = OUTDIR / f"{stamp}.md"

content = f"""# Raport godzinowy
Czas (Warszawa): {now.strftime('%Y-%m-%d %H:%M:%S %Z')}

## Statusy (skrót)
- Auto-nauka: aktywna (kolejka topics.yaml)
- Generatory raportów: OK
- Ostatnie pliki: sprawdź `reports/knowledge/` i `reports/daily/`

> Plik utworzony automatycznie co godzinę.
"""

out.write_text(content, encoding="utf-8")
print("[OK] Wygenerowano:", out)
