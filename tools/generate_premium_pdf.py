# Generate a premium PDF brochure using reportlab
# Reads pdf/config.json and pulls logo from assets/logos/
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path
import json, sys, datetime

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "pdf" / "config.json"
LOGOS = ROOT / "assets" / "logos"
FONTS = ROOT / "assets" / "fonts"
OUT   = ROOT / "pdf"

# try load DejaVu Serif, fallback to Times-Roman
FONT_NAME = "DejaVuSerif"
ttf = FONTS / "DejaVuSerif.ttf"
if ttf.exists():
    pdfmetrics.registerFont(TTFont(FONT_NAME, str(ttf)))
else:
    FONT_NAME = "Times-Roman"

def draw_header(c, title, subtitle, logo_path=None):
    width, height = A4
    c.setFillColor(black)
    c.setFont(FONT_NAME, 18)
    c.drawString(25*mm, height-25*mm, title)
    c.setFont(FONT_NAME, 11)
    c.drawString(25*mm, height-32*mm, subtitle)
    if logo_path and Path(logo_path).exists():
        try:
            c.drawImage(str(logo_path), width-55*mm, height-35*mm, width=30*mm, preserveAspectRatio=True, mask='auto')
        except Exception:
            pass
    # line
    c.line(20*mm, height-36*mm, width-20*mm, height-36*mm)

def draw_footer(c, page_num, contact):
    width, _ = A4
    c.setFont(FONT_NAME, 9)
    txt = f"{contact}    •    Strona {page_num}"
    c.drawRightString(width-20*mm, 12*mm, txt)

def draw_section(c, y, title, bullet_points):
    width, height = A4
    c.setFont(FONT_NAME, 13)
    c.drawString(25*mm, y, title)
    y -= 6*mm
    c.setFont(FONT_NAME, 11)
    for b in bullet_points:
        for line in wrap_text(b, 90):
            c.drawString(30*mm, y, f"• {line}")
            y -= 6*mm
        y -= 2*mm
    return y

def wrap_text(text, length=90):
    words = text.split()
    line = []
    for w in words:
        line.append(w)
        if sum(len(x)+1 for x in line) > length:
            yield " ".join(line)
            line = []
    if line:
        yield " ".join(line)

def main():
    project = sys.argv[1] if len(sys.argv) > 1 else "projects/Bezpieczny_Pieszy"
    cfg = {
        "title": "Stowarzyszenie Polska Potęga Bezpieczeństwa — Projekt premium",
        "subtitle": "KV + cel + KPI + pakiety sponsorskie + harmonogram + ewaluacja",
        "contact": "www.stowarzyszenieppb.pl • kontakt@stowarzyszenieppb.pl",
        "logo": None,
        "sections": [
            {"title":"Executive summary","bullets":["Problem i cel (SMART)","Grupy docelowe i insight","KPIs i spodziewane rezultaty"]},
            {"title":"Plan działań","bullets":["Edukacja w szkołach: scenariusze, odblaski","Kampania media: OOH/online/PR","Produkty: plakaty, ulotki, spoty"]},
            {"title":"Pakiety sponsorskie","bullets":["Mecenas / Partner Główny / Wspierający / Lokalny","Korzyści: branding, zasięgi, AVE, raport ROI"]},
            {"title":"Ewaluacja i ryzyka","bullets":["Ankiety pre/post, KPI media, dokumentacja foto/wideo","Zgodność: RODO, licencje, BHP eventów"]},
        ]
    }
    if CONFIG.exists():
        try:
            cfg.update(json.loads(CONFIG.read_text(encoding="utf-8")))
        except Exception:
            pass
    # logo pick
    logo = cfg.get("logo")
    if not logo:
        # pick first image-like file from logos
        for ext in [".png",".jpg",".jpeg",".pdf"]:
            for p in LOGOS.glob(f"*{ext}"):
                logo = p
                break
            if logo: break

    now = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    proj_name = Path(project).name.replace("_"," ")
    out_path = OUT / f"PREMIUM_{proj_name}_{now}.pdf"

    c = canvas.Canvas(str(out_path), pagesize=A4)
    draw_header(c, cfg.get("title", proj_name), cfg.get("subtitle",""), logo)
    y = A4[1]-45*mm
    for sec in cfg.get("sections",[]):
        y = draw_section(c, y, sec.get("title","Sekcja"), sec.get("bullets",[]))
        y -= 4*mm
        if y < 40*mm:
            draw_footer(c, c.getPageNumber(), cfg.get("contact",""))
            c.showPage()
            draw_header(c, cfg.get("title", proj_name), cfg.get("subtitle",""), logo)
            y = A4[1]-45*mm
    draw_footer(c, c.getPageNumber(), cfg.get("contact",""))
    c.save()
    print("[OK] PDF zapisany:", out_path)

if __name__ == "__main__":
    main()
