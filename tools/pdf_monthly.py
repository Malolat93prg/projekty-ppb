from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
OUT = Path("reports/monthly"); OUT.mkdir(parents=True, exist_ok=True)
now = datetime.now(ZoneInfo("Europe/Warsaw"))
path = OUT / f"PPB_Monthly_{now.strftime('%Y-%m')}.pdf"
c = canvas.Canvas(str(path), pagesize=A4)
c.setFont("Helvetica", 14); c.drawString(50, 800, "PPB — Miesięczny raport (demo)")
c.save(); print("[monthly] wrote", path)
