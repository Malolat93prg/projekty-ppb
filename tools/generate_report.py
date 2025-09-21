from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
import argparse

WARS = ZoneInfo("Europe/Warsaw")

def write(path: Path, title: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(WARS).strftime("%Y-%m-%d %H:%M")
    content = f"""# {title}
**Czas (Europe/Warsaw):** {ts}

## Status projektów
- Bezpieczny Pieszy — OK
- Zwolnij przy przejściu — OK
- Odblask ratuje życie — OK

"""
    path.write_text(content, encoding="utf-8")
    print("Wrote", path)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["hourly","daily","weekly"], required=True)
    args = ap.parse_args()

    now = datetime.now(WARS)
    if args.mode == "hourly":
        out = Path("reports/hourly") / f"PPB_hourly_{now.strftime('%Y-%m-%d_%H')}.md"
        write(out, "PPB – Raport godzinowy")
    elif args.mode == "daily":
        out = Path("reports/daily") / f"PPB_daily_{now.strftime('%Y-%m-%d')}.md"
        write(out, "PPB – Raport dzienny")
    else:
        out = Path("reports/weekly") / f"PPB_weekly_{now.strftime('%Y-%m-%d')}.md"
        write(out, "PPB – Raport tygodniowy")

if __name__ == "__main__":
    main()
