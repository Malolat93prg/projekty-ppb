#!/usr/bin/env python3
"""
Generate a monthly PDF summary using ReportLab.
- Reads basic project info from projects/projects.yaml (if available)
- Includes last daily report snippet from reports/daily (if available)
- Writes PDF to reports/monthly/PPB_Monthly_<YYYY-MM>.pdf
This script is defensive — if inputs are missing, it still generates a PDF.
"""
from __future__ import annotations
import os
from glob import glob
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path

# Lightweight deps only
try:
    import yaml  # PyYAML
except Exception:
    yaml = None

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parents[1]  # repo root (assumes tools/)
OUT_DIR = ROOT / "reports" / "monthly"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Try load custom font if present, otherwise use default
FONT_PATH = ROOT / "assets" / "fonts" / "NotoSans-Regular.ttf"
if FONT_PATH.exists():
    try:
        pdfmetrics.registerFont(TTFont("NotoSans", str(FONT_PATH)))
        BASE_FONT = "NotoSans"
    except Exception:
        BASE_FONT = "Helvetica"
else:
    BASE_FONT = "Helvetica"

def load_projects():
    yml = ROOT / "projects" / "projects.yaml"
    if yaml and yml.exists():
        try:
            return yaml.safe_load(yml.read_text(encoding="utf-8")) or {}
        except Exception:
            return {}
    return {}

def last_daily_snippet():
    daily_dir = ROOT / "reports" / "daily"
    if not daily_dir.exists():
        return None
    mds = sorted(daily_dir.glob("*.md"), reverse=True)
    if not mds:
        return None
    # Return first non-empty 40 lines
    text = mds[0].read_text(encoding="utf-8", errors="ignore")
    snippet = "\n".join([ln for ln in text.splitlines()[:40] if ln.strip()])
    return snippet or None

def build_pdf():
    now = datetime.now(ZoneInfo("Europe/Warsaw"))
    month_tag = now.strftime("%Y-%m")
    out_file = OUT_DIR / f"PPB_Monthly_{month_tag}.pdf"

    doc = SimpleDocTemplate(
        str(out_file),
        pagesize=A4,
        leftMargin=36, rightMargin=36, topMargin=48, bottomMargin=36,
        title=f"PPB Monthly Report {month_tag}",
        author="PPB Bot"
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("TitleXL", parent=styles["Title"], fontName=BASE_FONT, fontSize=24))
    styles.add(ParagraphStyle("H2", parent=styles["Heading2"], fontName=BASE_FONT, spaceBefore=12))
    styles.add(ParagraphStyle("Body", parent=styles["BodyText"], fontName=BASE_FONT, leading=14))
    styles.add(ParagraphStyle("Small", parent=styles["BodyText"], fontName=BASE_FONT, fontSize=8, textColor=colors.grey))

    story = []
    story.append(Paragraph("Miesięczne podsumowanie – PPB", styles["TitleXL"]))
    story.append(Paragraph(now.strftime("%B %Y, strefa: Europe/Warsaw"), styles["Small"]))
    story.append(Spacer(1, 12))

    # Projects overview
    story.append(Paragraph("Przegląd projektów", styles["H2"]))
    projects = load_projects()
    if isinstance(projects, dict) and projects.get("projects"):
        data = [["Projekt", "Status", "Postęp", "ETA"]]
        for p in projects["projects"]:
            name = p.get("name", "-")
            status = p.get("status", "-")
            progress = f"{p.get('progress', 0)}%"
            eta = p.get("eta", "-")
            data.append([name, status, progress, eta])
        tbl = Table(data, hAlign="LEFT", colWidths=[200, 100, 70, 100])
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
            ("TEXTCOLOR", (0,0), (-1,0), colors.black),
            ("FONTNAME", (0,0), (-1,0), BASE_FONT),
            ("GRID", (0,0), (-1,-1), 0.25, colors.grey),
            ("ALIGN", (2,1), (2,-1), "RIGHT"),
        ]))
        story.append(tbl)
    else:
        story.append(Paragraph("Brak zdefiniowanych projektów (projects/projects.yaml).", styles["Body"]))

    story.append(Spacer(1, 18))

    # Last daily snippet
    story.append(Paragraph("Ostatni dzienny raport – skrót", styles["H2"]))
    snippet = last_daily_snippet()
    if snippet:
        for line in snippet.splitlines():
            story.append(Paragraph(line.replace("<", "&lt;").replace(">", "&gt;"), styles["Body"]))
    else:
        story.append(Paragraph("Brak dziennych raportów w katalogu reports/daily.", styles["Body"]))

    story.append(Spacer(1, 18))
    story.append(Paragraph("Automatycznie wygenerowano w GitHub Actions.", styles["Small"]))

    doc.build(story)
    print(f"[OK] Zapisano: {out_file}")
    return out_file

if __name__ == "__main__":
    out = build_pdf()
    print(out)
