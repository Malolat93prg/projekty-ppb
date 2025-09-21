
import os
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import argparse
import pathlib

def load_projects():
    # proste wczytanie nagłówków z katalogu projects
    items = []
    p = pathlib.Path("projects")
    if not p.exists():
        return items
    for f in sorted(p.glob("*.md")):
        title = f.stem.replace("_"," ").title()
        items.append((title, f))
    return items

def make_report(mode: str):
    tz = ZoneInfo(os.environ.get("TZ","Europe/Warsaw"))
    now = datetime.now(tz)
    ts = now.strftime("%Y-%m-%d %H:%M:%S %Z")
    lines = []
    lines.append(f"# PPB – raport {mode}")
    lines.append("")
    lines.append(f"**Czas lokalny:** {ts}")
    lines.append("")
    lines.append("## Projekty")
    for title, f in load_projects():
        lines.append(f"- {title} ([{f}](../{f}))")
    lines.append("")
    lines.append("## Status")
    lines.append("- Generacja automatyczna przez GitHub Actions.")
    content = "\n".join(lines)
    return content, now

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["hourly","daily","weekly"], default="hourly")
    args = ap.parse_args()
    content, now = make_report(args.mode)
    sub = "hourly" if args.mode=="hourly" else ("daily" if args.mode=="daily" else "weekly")
    out_dir = pathlib.Path("reports") / sub
    out_dir.mkdir(parents=True, exist_ok=True)
    fname = out_dir / f"report-{now.strftime('%Y-%m-%d_%H%M')}.md"
    with open(fname, "w", encoding="utf-8") as f:
        f.write(content)
    # ostatnia kopia
    latest = pathlib.Path("reports") / f"latest_{sub}.md"
    with open(latest, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Wrote {fname}")
if __name__ == "__main__":
    main()
