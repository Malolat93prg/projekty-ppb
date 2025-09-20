import os, json, datetime, glob, math, random
import pytz
from send_telegram import send_telegram

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONFIG_PATH = os.path.join(ROOT, "config.json")
REPORTS_DIR = os.path.join(ROOT, "reports")
KNOW_DIR = os.path.join(ROOT, "knowledge")

DEFAULT = {
    "project_name": "Auto-nauka PPB",
    "timezone": "Europe/Warsaw",
    "modules": [
        "Prawo i administracja",
        "Zarządzanie i organizacja",
        "Marketing i reklama",
        "Fundraising i sponsorzy",
        "Edukacja i BRD",
        "Media i multimedia",
        "Rozwój strategiczny"
    ],
    "telegram": {"enabled": False, "token_env": "TELEGRAM_TOKEN", "chat_id_env": "TELEGRAM_CHAT_ID"},
    "panel_width": 17
}

def load_config():
    cfg = DEFAULT.copy()
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            user = json.load(f)
        for k, v in user.items():
            cfg[k] = v
    return cfg

def progress_bar(p, width=17):
    full = math.floor(p * width)
    empty = width - full
    return "█" * full + "-" * empty

def summarize_notes(limit=20):
    items = []
    for path in sorted(glob.glob(os.path.join(KNOW_DIR, "*"))):
        if os.path.isfile(path):
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    head = f.readline().strip()
            except Exception:
                head = ""
            items.append((os.path.basename(path), head))
    return items[:limit]

def main():
    cfg = load_config()
    os.makedirs(REPORTS_DIR, exist_ok=True)

    tz = pytz.timezone(cfg.get("timezone", "Europe/Warsaw"))
    now = datetime.datetime.now(tz)
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")

    # Prosta symulacja postępu (tu można wpiąć prawdziwe metryki)
    random.seed(now.hour)  # stabilne w obrębie godziny
    lines = []
    lines.append(f"# Raport auto-nauki — {cfg['project_name']}")
    lines.append(f"Stan na: {now_str} ({cfg.get('timezone')})\n")

    lines.append("```")
    width = int(cfg.get("panel_width", 17))
    for m in cfg["modules"]:
        pct = 0.30 + random.random() * 0.55  # 30–85%
        eta_days = max(1, int((1.0 - pct) * 10))
        bar = progress_bar(pct, width=width)
        lines.append(f"{m:26} [{bar}] {int(pct*100):>3}%   ETA: {eta_days} dni   🕒 {now.strftime('%H:%M')}")
    lines.append("```\n")

    notes = summarize_notes()
    if notes:
        lines.append("## Nowe / zaktualizowane notatki")
        for fname, head in notes:
            head = head if head else "(brak nagłówka)"
            lines.append(f"- **{fname}** — {head}")
        lines.append("")

    body = "\n".join(lines)
    out_md = os.path.join(REPORTS_DIR, "latest_report.md")
    with open(out_md, "w", encoding="utf-8") as f:
        f.write(body)

    # Telegram (opcjonalnie)
    tel = cfg.get("telegram", {})
    if tel.get("enabled"):
        token = os.getenv(tel.get("token_env", "TELEGRAM_TOKEN"))
        chat_id = os.getenv(tel.get("chat_id_env", "TELEGRAM_CHAT_ID"))
        if token and chat_id:
            msg = f"Auto-raport PPB: {now_str}"
            send_telegram(token, chat_id, msg)
            print("Wysłano powiadomienie Telegram.")
        else:
            print("Brak token/chat_id w secrets — pomijam Telegram.")
    else:
        print("Telegram wyłączony.")

    print("Zapisano:", out_md)

if __name__ == "__main__":
    main()