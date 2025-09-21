
import os, zipfile, pathlib
from datetime import datetime
from zoneinfo import ZoneInfo

def main():
    tz = ZoneInfo(os.environ.get("TZ","Europe/Warsaw"))
    now = datetime.now(tz)
    out_dir = pathlib.Path("reports/weekly")
    out_dir.mkdir(parents=True, exist_ok=True)
    zip_path = out_dir / f"weekly-{now.strftime('%Y-%m-%d_%H%M')}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for sub in ["reports/hourly","reports/daily"]:
            p = pathlib.Path(sub)
            if p.exists():
                for f in p.rglob("*.md"):
                    z.write(f, f.relative_to("."))
    print(f"Created {zip_path}")
if __name__ == "__main__":
    main()
