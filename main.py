# Imports
import glob
import pathlib
from fpdf import FPDF
import modules.pdf_helper as pdf_helper

paper = pdf_helper.get_paper("A4")
area = pdf_helper.calculate_area(paper)

columns = [
    {"ratio": 1},
    {"ratio": 2.5},
    {"ratio": 1.5},
    {"ratio": 1.5},
    {"ratio": 1.5},
]

column_settings = pdf_helper.get_column_settings(area, columns)

filepaths = glob.glob("files/xlsx/*.xlsx")

for filepath in filepaths:
    # Data
    filename = pathlib.Path(filepath).stem
    invoice_number, invoice_date = filename.split("-")

    # Document
    pdf = FPDF("portrait", "mm", paper["format"])
    pdf.add_page()

    # Page Titles
    pdf.set_font("Times", "B", 16)
    pdf.cell(0, 8, f"Invoice: #{invoice_number}", 0, 1)
    pdf.cell(0, 8, f"Date: {invoice_date}", 0, 1)
    pdf.ln(8)

    # Table Headers
    pdf.set_font("Times", "B", 10)

    for index, settings in enumerate(column_settings, start=1):
        pdf.cell(settings["width"], 8, f"Column {index}", 1)

    pdf.ln()

    # Output File
    pdf.output(f"files/pdf/{filename}.pdf")
