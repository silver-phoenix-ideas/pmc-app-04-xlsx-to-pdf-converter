import glob
import pathlib
from fpdf import FPDF

filepaths = glob.glob("files/xlsx/*.xlsx")

for filepath in filepaths:
    filename = pathlib.Path(filepath).stem

    pdf = FPDF("portrait", "mm", "A4")
    pdf.set_font("Times", "B", 16)
    pdf.add_page()
    pdf.output(f"files/pdf/{filename}.pdf")
