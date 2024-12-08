from fpdf import FPDF


def table_header(
    pdf: FPDF,
    title: str,
    settings: dict,
    line_height: int
) -> None:
    pdf.cell(
        w=settings["width"],
        h=line_height,
        txt=title,
        border=1
    )
