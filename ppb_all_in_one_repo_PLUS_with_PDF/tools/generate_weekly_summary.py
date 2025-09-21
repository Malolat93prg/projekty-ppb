# PPB — Weekly summary builder (collect last 7 days)
import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path

TZ = ZoneInfo(os.environ.get("TZ", "Europe/Warsaw"))
ROOT = Path(__file__).resolve().parents[1]
WEEKLY_DIR = ROOT / "reports" / "weekly"
WEEKLY_DIR.mkdir(parents=True, exist_ok=True)

def collect_markdowns(subdir, days=7):
    base = ROOT / subdir
    if not base.exists():
        return []
    cutoff = datetime.now(TZ) - timedelta(days=days)
    items = []
    for p in sorted(base.glob("*.md")):
        try:
            ts = datetime.fromtimestamp(p.stat().st_mtime, TZ)
            if ts >= cutoff:
                items.append(p)
        except Exception:
            pass
    return items

now = datetime.now(TZ)
title_date = now.strftime("%Y-%m-%d")
outfile = WEEKLY_DIR / f"{title_date}-weekly-summary.md"

lines = [f"# Tygodniowe podsumowanie — {now.strftime('%Y-%m-%d %H:%M (%Z)')}\n"]
lines.append("## Moduły wiedzy (ostatnie 7 dni)")
for p in collect_markdowns("reports/knowledge", days=7):
    rel = p.relative_to(ROOT).as_posix()
    lines.append(f"- [{p.stem}]({rel})")

lines.append("\n## Raporty dzienne (ostatnie 7 dni)")
for p in collect_markdowns("reports/daily", days=7):
    rel = p.relative_to(ROOT).as_posix()
    lines.append(f"- [{p.stem}]({rel})")

lines.append("\n## Raporty godzinowe (ostatnie 24h)")
for p in collect_markdowns("reports/hourly", days=1):
    rel = p.relative_to(ROOT).as_posix()
    lines.append(f"- [{p.stem}]({rel})")

outfile.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("[OK] Zapisano tygodniowe podsumowanie:", outfile)

# Save path for email_send.py
(ROOT / "reports" / "weekly" / "_latest_path.txt").write_text(str(outfile), encoding="utf-8")
