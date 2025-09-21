import os, yaml, json
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path

TZ = ZoneInfo(os.environ.get("TZ", "Europe/Warsaw"))
ROOT = Path(__file__).resolve().parents[1]
TOPICS = ROOT / "knowledge" / "topics.yaml"
STATE  = ROOT / "knowledge" / ".state.daily.json"
OUTDIR = ROOT / "reports" / "knowledge"
OUTDIR.mkdir(parents=True, exist_ok=True)

def load_topics():
    with open(TOPICS, "r", encoding="utf-8") as f:
        txt = f.read()
        if "\n- " in txt or txt.strip().startswith("- "):
            lines = [ln[2:].strip() for ln in txt.splitlines() if ln.strip().startswith("- ")]
            return [ln for ln in lines if ln]
        f.seek(0)
        return yaml.safe_load(f) or []

def load_state():
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"index": -1, "cycle": 1}

def save_state(state):
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

def normalize_title(topic):
    return topic.split(" — ")[0].strip()

def main():
    topics = load_topics()
    if not topics:
        raise SystemExit("Brak tematów w knowledge/topics.yaml")

    st = load_state()
    idx = st["index"] + 1
    cycle = st.get("cycle", 1)

    if idx >= len(topics):
        idx = 0
        cycle += 1

    topic_full = topics[idx]
    st["index"] = idx
    st["cycle"] = cycle
    save_state(st)

    now = datetime.now(TZ)
    date_tag = now.strftime("%Y-%m-%d")
    title = normalize_title(topic_full)

    header = f"{title} — moduł dzienny ({date_tag}) — cykl {cycle}"
    body = f"""# {header}

**Zakres:** {topic_full}

## Najważniejsze założenia (skrót 3–5 punktów)
- TODO (uzupełnić na podstawie źródeł).

## Co zgłębiamy dziś (źródła)
- Oficjalne wytyczne, normy, dobre praktyki, narzędzia.

## Zastosowanie u nas (quick wins)
- Lista szybkich wdrożeń do: Bezpieczny Pieszy, Zwolnij przy przejściu, Odblask ratuje życie.

> Plik wygenerowany automatycznie (auto-nauka dzienna), cykl {cycle}.
"""

    out = OUTDIR / f"{date_tag}-{title.lower().replace(' ', '_')}-cykl_{cycle}.md"
    out.write_text(body, encoding="utf-8")

    # indeks
    items = sorted(OUTDIR.glob("*.md"))
    index = OUTDIR / "README.md"
    lines = [f"# Moduły wiedzy — dzienne\n\nOstatnia aktualizacja: {now.strftime('%Y-%m-%d %H:%M (%Z)')}\n\n"]
    for p in items:
        rel = p.relative_to(ROOT).as_posix()
        lines.append(f"- [{p.stem}]({rel})")
    index.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"[OK] Wygenerowano moduł dzienny: {out.name} (idx={idx}, cykl={cycle})")

if __name__ == "__main__":
    main()
