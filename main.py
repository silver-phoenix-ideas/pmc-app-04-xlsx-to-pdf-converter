# Imports
import glob
import pathlib
import pandas as pd
from fpdf import FPDF
import modules.pdf_helper as pdf_helper
import modules.components as components

paper = pdf_helper.get_paper("A4")
area = pdf_helper.calculate_area(paper)

columns = [
    {"ratio": 1, "data_type": "number"},
    {"ratio": 2.5, "data_type": "string"},
    {"ratio": 1.5, "data_type": "number"},
    {"ratio": 1.5, "data_type": "currency"},
    {"ratio": 1.5, "data_type": "currency"},
]

column_settings = pdf_helper.get_column_settings(area, columns)

filepaths = glob.glob("files/xlsx/*.xlsx")

for filepath in filepaths:
    # Data
    filename = pathlib.Path(filepath).stem
    invoice_number, invoice_date = filename.split("-")
    df = pd.read_excel(filepath)
    column_titles = [column.replace("_", " ").title() for column in df.columns]
    total_cost = df["total_price"].sum()

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

    for title, settings in zip(column_titles, column_settings):
        components.table_header(pdf, title, settings, 8)

    pdf.ln()

    # Invoice Items
    pdf.set_font("Times", "", 10)
    for index, row in df.iterrows():
        for content, settings in zip(row, column_settings):
            components.table_cell(pdf, content, settings, 8)

        pdf.ln()

    # Invoice Total
    for index, settings in enumerate(column_settings, start=1):
        if index != len(column_settings):
            components.table_cell(pdf, "", settings, 8)
        else:
            components.table_cell(pdf, total_cost, settings, 8)

    pdf.ln(16)

    # Output File
    pdf.output(f"files/pdf/{filename}.pdf")
