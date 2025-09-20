import os, json, datetime, glob, random, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
KNOW = ROOT / "knowledge"
CONFIG = ROOT / "config.json"

DEFAULT = {
    "project_name": "Auto-nauka PPB",
    "timezone_label": "Europe/Warsaw",
    "modules": [
        "Prawo i administracja",
        "Zarządzanie i organizacja",
        "Marketing i reklama",
        "Fundraising i sponsorzy",
        "Edukacja i BRD",
        "Media i multimedia",
        "Rozwój strategiczny",
    ],
    "panel_width": 17
}

def load_cfg():
    if CONFIG.exists():
        try:
            return json.loads(CONFIG.read_text(encoding="utf-8"))
        except Exception:
            pass
    return DEFAULT

def bar(p, w=17):
    full = int(p * w)
    return "█"*full + "-"*(w-full)

def summarize_notes(limit=20):
    items = []
    if KNOW.exists():
        for p in sorted(KNOW.iterdir()):
            if p.is_file():
                try:
                    head = p.read_text(encoding="utf-8", errors="ignore").splitlines()[0].strip()
                except Exception:
                    head = ""
                items.append((p.name, head or "(brak nagłówka)"))
    return items[:limit]

def main():
    cfg = load_cfg()
    REPORTS.mkdir(parents=True, exist_ok=True)
    KNOW.mkdir(parents=True, exist_ok=True)

    now = datetime.datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")

    random.seed(now.hour)
    w = int(cfg.get("panel_width", 17))

    lines = [
        f"# Raport auto-nauki — {cfg['project_name']}",
        f"Stan na: {now_str} ({cfg.get('timezone_label','Europe/Warsaw')})",
        "",
        "```"
    ]
    for m in cfg["modules"]:
        pct = 0.30 + random.random()*0.55
        eta_days = max(1, int((1.0 - pct) * 10))
        lines.append(f"{m:26} [{bar(pct,w)}] {int(pct*100):>3}%   ETA: {eta_days} dni   🕒 {now.strftime('%H:%M')}")
    lines.append("```")
    lines.append("")

    notes = summarize_notes()
    if notes:
        lines.append("## Nowe / zaktualizowane notatki")
        for fname, head in notes:
            lines.append(f"- **{fname}** — {head}")
        lines.append("")

    out = REPORTS / "latest_report.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print("Zapisano:", out)

if __name__ == "__main__":
    main()
