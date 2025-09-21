from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from datetime import datetime

def generate_monthly_pdf():
    os.makedirs("reports", exist_ok=True)
    filename = f"reports/monthly_report.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 20)
    c.drawString(100, height - 100, "Miesięczny Raport PPB")
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 140, f"Data wygenerowania: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    c.setFont("Helvetica", 10)
    c.drawString(100, height - 180, "Podsumowanie działań:")
    c.drawString(120, height - 200, "- Raporty godzinowe i dzienne zostały wygenerowane automatycznie.")
    c.drawString(120, height - 220, "- Raport tygodniowy został wysłany zgodnie z harmonogramem.")
    c.drawString(120, height - 240, "- Projekty i wiedza zostały zaktualizowane w repozytorium.")

    c.save()

if __name__ == "__main__":
    generate_monthly_pdf()
