
import os
from datetime import datetime
from dateutil import tz
from pathlib import Path
import yaml

# ReportLab
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors

# --- Time gate (only 1st day 20:00-20:59 Warsaw unless FORCE=true) ---
force = str(os.environ.get("FORCE", "")).lower() in ("1", "true", "yes", "on")
if not force:
    warsaw = tz.gettz("Europe/Warsaw")
    now = datetime.now(warsaw)
    if not (now.day == 1 and now.hour == 20):
        print(f"[monthly] Gate: not 1st day 20:xx Warsaw (now={now}). Exiting gracefully.")
        raise SystemExit(0)

# --- Load optional projects file ---
projects_yaml = Path("projects/projects.yaml")
projects = []
if projects_yaml.exists():
    try:
        projects = yaml.safe_load(projects_yaml.read_text(encoding="utf-8")) or []
        if not isinstance(projects, list):
            projects = []
    except Exception as e:
        print(f"[monthly] Could not parse projects.yaml: {e}")

# --- Prepare output path ---
out_dir = Path("reports/monthly")
out_dir.mkdir(parents=True, exist_ok=True)
ts = datetime.now(tz.gettz("Europe/Warsaw")).strftime("%Y-%m")
out_file = out_dir / f"PPB_Monthly_{ts}.pdf"

# --- Canvas ---
c = canvas.Canvas(str(out_file), pagesize=A4)
W, H = A4

# Try to use NotoSans if present
font_path = Path("assets/fonts/NotoSans-Regular.ttf")
if font_path.exists():
    from reportlab.pdfbase import ttfonts, pdfmetrics
    pdfmetrics.registerFont(ttfonts.TTFont("NotoSans", str(font_path)))
    FONT = "NotoSans"
else:
    FONT = "Helvetica"

def hline(y):
    c.setStrokeColor(colors.HexColor("#999999"))
    c.line(2*cm, y, W-2*cm, y)

def text(x, y, s, size=12, bold=False, color=colors.black):
    c.setFillColor(color)
    c.setFont(FONT, size)
    c.drawString(x, y, s)

# --- Header ---
y = H - 2.5*cm
text(2*cm, y, "Polska Potęga Bezpieczeństwa — Miesięczny raport", 16)
y -= 0.8*cm
text(2*cm, y, f"Miesiąc: {ts}", 12, color=colors.HexColor("#444444"))
hline(y-0.3*cm)
y -= 1.2*cm

# --- Summary ---
text(2*cm, y, "Podsumowanie", 14); y -= 0.8*cm
summary = [
    "• Postęp projektów aktualizowany automatycznie.",
    "• Ten PDF generowany 1-szego dnia miesiąca o 20:05 czasu Warszawy.",
    "• Dane pochodzą z repo: projekty, raporty, statusy."
]
for line in summary:
    text(2.2*cm, y, line, 11); y -= 0.6*cm
y -= 0.3*cm
hline(y); y -= 1.0*cm

# --- Projects section ---
text(2*cm, y, "Projekty", 14); y -= 0.8*cm
if not projects:
    text(2.2*cm, y, "Brak zdefiniowanych projektów (projects/projects.yaml).", 11, color=colors.HexColor("#aa0000"))
    y -= 0.8*cm
else:
    for p in projects:
        name = p.get("name","(bez nazwy)")
        progress = p.get("progress", 0)
        eta = p.get("eta","-")
        text(2.2*cm, y, f"{name} — {progress}% (ETA: {eta})", 11); y -= 0.6*cm

# --- Footer ---
c.setFillColor(colors.HexColor("#666666"))
c.setFont(FONT, 9)
c.drawRightString(W-2*cm, 1.5*cm, f"Wygenerowano: {datetime.now(tz.gettz('Europe/Warsaw')).strftime('%Y-%m-%d %H:%M')}  |  PPB")

c.showPage()
c.save()
print(f"[monthly] Saved {out_file}")
