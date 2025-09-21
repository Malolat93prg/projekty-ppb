# PPB — generator dziennego raportu (20:00)
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
import re

TZ = ZoneInfo(os.environ.get("TZ", "Europe/Warsaw"))
ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "reports" / "daily"
OUTDIR.mkdir(parents=True, exist_ok=True)

now = datetime.now(TZ)
date_tag = now.strftime("%Y-%m-%d")
out_file = OUTDIR / f"{date_tag}-daily-report.md"

# Nagłówek
header = f"""# Raport dzienny — {now.strftime('%Y-%m-%d %H:%M (%Z)')}

Ten raport zawiera podsumowanie dzisiejszych działań i **podgląd najnowszego modułu wiedzy**.
"""
out_file.write_text(header, encoding="utf-8")

# Baner z najnowszym modułem wiedzy
from pathlib import Path as _PPBPath
import re as _re
_ROOT = _PPBPath(__file__).resolve().parents[1]
_KNOW_DIR = _ROOT / "reports" / "knowledge"

def _ppb_extract_preview(md_text, max_chars=900):
    sections = _re.split(r'\n## ', md_text)
    pick = sections[:3]
    preview = '\n## '.join(pick)
    preview = _re.sub(r'\n{3,}', '\n\n', preview).strip()
    if len(preview) > max_chars:
        preview = preview[:max_chars].rsplit(' ', 1)[0] + '…'
    return preview

try:
    if _KNOW_DIR.exists():
        _items = sorted(_KNOW_DIR.glob("*.md"))
        if _items:
            _latest = _items[-1]
            _rel = _latest.relative_to(_ROOT).as_posix()
            _txt = _latest.read_text(encoding="utf-8", errors="ignore")
            _preview = _ppb_extract_preview(_txt)
            _banner = (
                "\n\n---\n"
                "### 🧠 Moduł wiedzy (auto, dzienny) — podgląd\n\n"
                f"{_preview}\n\n"
                f"**Pełny moduł:** [{_latest.stem}]({_rel})\n"
            )
            with open(out_file, "a", encoding="utf-8") as _f:
                _f.write(_banner)
except Exception as _e:
    print("[WARN] Baner modułu wiedzy nie został dodany:", _e)

# Stopka
with open(out_file, "a", encoding="utf-8") as f:
    f.write("\n---\n*Wygenerowano automatycznie przez workflow o 20:00 (Europe/Warsaw).*\n")
print("[OK] Zapisano:", out_file)
