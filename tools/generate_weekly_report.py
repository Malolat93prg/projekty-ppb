from __future__ import annotations
import os, sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

def last_sunday_warsaw(now: datetime) -> datetime:
    # ensure we get the Sunday of the current ISO week (or today, if Sunday)
    dow = now.weekday()  # Monday=0 ... Sunday=6
    days_since_sun = (dow - 6) % 7  # 0 when Sunday
    return (now - timedelta(days=days_since_sun)).replace(hour=20, minute=5, second=0, microsecond=0)

def main():
    tz_name = os.environ.get("TZ", "Europe/Warsaw")
    tz = ZoneInfo(tz_name)
    now = datetime.now(tz)

    sunday = last_sunday_warsaw(now)
    date_tag = sunday.date().isoformat()
    os.makedirs("reports", exist_ok=True)
    path = f"reports/{date_tag}-weekly-summary.md"

    body = f"""# Weekly Summary — {date_tag}

**Timezone:** {tz_name} | **Generated:** {now:%Y-%m-%d %H:%M:%S %Z}

## Highlights
- Placeholder highlights (add more sources as needed).

## Projects
- Bezpieczny Pieszy — status: in progress
- Zwolnij przy przejściu — status: in progress
- Odblask ratuje życie — status: in progress

## Actions Next Week
- [ ] Review tasks and priorities
- [ ] Prepare assets
- [ ] Update stakeholders
"""

    with open(path, "w", encoding="utf-8") as f:
        f.write(body)

    print(f"[OK] Generated {path}")

if __name__ == "__main__":
    main()