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
        border=1,
        align=settings["align"]
    )


def table_cell(
        pdf: FPDF,
        content: str | int | float,
        settings: dict,
        line_height: int
) -> None:
    pdf.cell(
        w=settings["width"],
        h=line_height,
        txt=format_content(content, settings["data_type"]),
        border=1,
        align=settings["align"]
    )


def format_content(content: str | int | float, data_type: str) -> str:
    match data_type:
        case "currency":
            try:
                content = "{:.2f}".format(content)
            except ValueError:
                content = str(content)
        case _:
            content = str(content)

    return content
