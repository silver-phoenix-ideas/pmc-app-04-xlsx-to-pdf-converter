def get_paper(paper_format: str = "A4") -> dict:
    paper_format = paper_format.casefold()

    paper = {
        "format": paper_format,
        "margin_top": 10,
        "margin_right": 10,
        "margin_bottom": 20,
        "margin_left": 10
    }

    match paper_format:
        case "a3":
            paper["width"] = 297
            paper["height"] = 420
        case "a4":
            paper["width"] = 210
            paper["height"] = 297
        case "a5":
            paper["width"] = 148
            paper["height"] = 210
        case "letter":
            paper["width"] = 216
            paper["height"] = 279
        case "legal":
            paper["width"] = 216
            paper["height"] = 356
        case _:
            paper["width"] = 0
            paper["height"] = 0

    return paper


def calculate_area(paper: dict) -> dict:
    area = {
        "top": paper["margin_top"],
        "bottom": paper["height"] - paper["margin_bottom"],
        "left": paper["margin_left"],
        "right": paper["width"] - paper["margin_right"]
    }

    return area


def get_column_settings(area: dict, columns: list) -> list:
    area_width = area["right"] - area["left"]
    ratios = [column["ratio"] for column in columns]
    coefficient = area_width / sum(ratios)

    for column in columns:
        column["width"] = column["ratio"] * coefficient

    return columns
