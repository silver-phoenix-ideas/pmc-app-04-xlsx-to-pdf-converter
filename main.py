import glob
import pathlib
from fpdf import FPDF

filepaths = glob.glob("files/xlsx/*.xlsx")

for filepath in filepaths:
    filename = pathlib.Path(filepath).stem
    invoice_number, invoice_date = filename.split("-")

    pdf = FPDF("portrait", "mm", "A4")
    pdf.set_font("Times", "B", 16)

    pdf.add_page()
    pdf.cell(0, 8, f"Invoice: #{invoice_number}", 0, 1)
    pdf.cell(0, 8, f"Date: {invoice_date}", 0, 1)
    pdf.output(f"files/pdf/{filename}.pdf")
