# Imports
import glob
import pathlib
import pandas as pd
from fpdf import FPDF
import modules.pdf_helper as pdf_helper
import modules.components as components

# Sizes
base = 8
line_height = base
title_size = int(base * 2)
summary_size = int(base * 1.5)
item_size = int(base * 1.25)
image_size = int(base * 0.75)

paper = pdf_helper.get_paper("A4")
area = pdf_helper.calculate_area(paper)

columns = [
    {"ratio": 1, "align": "L", "data_type": "number"},
    {"ratio": 2.5, "align": "L", "data_type": "string"},
    {"ratio": 1.5, "align": "C", "data_type": "number"},
    {"ratio": 1.5, "align": "R", "data_type": "currency"},
    {"ratio": 1.5, "align": "R", "data_type": "currency"},
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
    pdf.set_font("Times", "B", title_size)
    pdf.cell(0, line_height, f"Invoice: #{invoice_number}", 0, 1)
    pdf.cell(0, line_height, f"Date: {invoice_date}", 0, 1)
    pdf.ln(line_height)

    # Table Headers
    pdf.set_font("Times", "B", item_size)

    for title, settings in zip(column_titles, column_settings):
        components.table_header(pdf, title, settings, line_height)

    pdf.ln()

    # Invoice Items
    pdf.set_font("Times", "", item_size)
    for index, row in df.iterrows():
        for content, settings in zip(row, column_settings):
            components.table_cell(pdf, content, settings, line_height)

        pdf.ln()

    # Invoice Total
    for index, settings in enumerate(column_settings, start=1):
        if index != len(column_settings):
            components.table_cell(pdf, "", settings, line_height)
        else:
            components.table_cell(pdf, total_cost, settings, line_height)

    pdf.ln(line_height * 2)

    # Summary Text
    pdf.set_font("Times", "B", summary_size)
    pdf.cell(0, line_height, "Total cost is {:.2f}".format(total_cost), 0, 1)
    pdf.cell(summary_size * 2, line_height, "PythonHow")
    pdf.image("pythonhow.png", h=image_size)

    # Output File
    pdf.output(f"files/pdf/{filename}.pdf")
