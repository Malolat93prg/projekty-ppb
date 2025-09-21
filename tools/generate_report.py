# tools/generate_report.py
# Generator raportów: tworzy reports/latest_report.md + archiwum reports/report-YYYY-MM-DD_HHMM.md
# Czyta dane z:
#  - knowledge/learning_plan.md (plan nauki, opcjonalnie)
#  - projects/status.json      (status projektów, opcjonalnie)
# Nie wymaga dodatkowych bibliotek.

import os
import json
from pathlib import Path
from datetime import datetime
try:
    from zoneinfo import ZoneInfo  # Python 3.9+
except Exception:
    ZoneInfo = None

REPO_ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = REPO_ROOT / "reports"
KNOWLEDGE_PLAN = REPO_ROOT / "knowledge" / "learning_plan.md"
PROJECTS_STATUS = REPO_ROOT / "projects" / "status.json"

TZ = os.environ.get("TZ", "Europe/Warsaw")

def now_pl():
    if ZoneInfo:
        return datetime.now(ZoneInfo(TZ))
    return datetime.now()

def safe_read_text(path: Path, fallback: str = "") -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return fallback

def load_projects_status():
    # Spodziewany format:
    # {
    #   "Bezpieczny Pieszy": {"progress": 42, "eta": "2025-09-21 20:00"},
    #   "Zwolnij przy przejściu": {"progress": 18, "eta": "2025-09-22 12:00"},
    #   "Odblask ratuje życie": {"progress": 5, "eta": "2025-09-25 18:30"}
    # }
    if PROJECTS_STATUS.exists():
        try:
            data = json.loads(PROJECTS_STATUS.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return data
        except Exception:
            pass
    # Domyślne wartości, jeśli pliku brak:
    return {
        "Bezpieczny Pieszy": {"progress": 0, "eta": "-"},
        "Zwolnij przy przejściu": {"progress": 0, "eta": "-"},
        "Odblask ratuje życie": {"progress": 0, "eta": "-"}
    }

def projects_table(data: dict) -> str:
    lines = []
    lines.append("| Projekt | Postęp | ETA |")
    lines.append("|--------|--------|-----|")
    for name, meta in data.items():
        prog = f"{int(meta.get('progress', 0))}%"
        eta = str(meta.get('eta', "-"))
        lines.append(f"| {name} | {prog} | {eta} |")
    return "\n".join(lines)

def make_report() -> str:
    now = now_pl()
    ts_date = now.strftime("%Y-%m-%d")
    ts_time = now.strftime("%H:%M")
    ts_file = now.strftime("%Y-%m-%d_%H%M")

    learning = safe_read_text(
        KNOWLEDGE_PLAN,
        fallback=(
            "- (Uzupełnij `knowledge/learning_plan.md` – tu pokażę zarys planu nauki)\n"
            "- Sekcje: Social media, Fundraising, BRD, Produkcja materiałów, Prawo dla NGO, Sponsorzy\n"
        )
    )
    pstatus = load_projects_status()
    ptable = projects_table(pstatus)

    content = f"""# Raport godzinowy — PPB
**Data:** {ts_date}  **Godzina (Europe/Warsaw):** {ts_time}

## 1) Status projektów
{ptable}

## 2) Plan nauki (wyciąg)
{learning}

## 3) Najbliższe działania (auto-sugestie)
- Aktualizacja statusu projektów w `projects/status.json`.
- Rozszerzenie `knowledge/learning_plan.md` o dzisiejsze tematy.
- Przygotowanie mockupów i KPI do raportu dziennego (20:00).

*Raport generowany automatycznie przez `tools/generate_report.py`.*
"""
    return content, ts_file

def write_reports(content: str, ts_file: str):
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    latest = REPORTS_DIR / "latest_report.md"
    archive = REPORTS_DIR / f"report-{ts_file}.md"
    latest.write_text(content, encoding="utf-8")
    archive.write_text(content, encoding="utf-8")

def main():
    content, ts_file = make_report()
    write_reports(content, ts_file)
    print("Report generated:", f"reports/report-{ts_file}.md")

if __name__ == "__main__":
    main()
