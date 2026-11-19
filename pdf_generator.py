"""Генератор PDF-отчётов: бесплатный лид-магнит и платный полный разбор."""
import os
from fpdf import FPDF
from matrix_calculator import calculate_matrix, get_arcana_text, get_arcana_name, POSITIONS

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


# Пыльное розовое золото + кремовый
ROSE = (183, 110, 121)
GOLD = (181, 141, 90)
DARK = (74, 54, 53)
GRAY = (139, 119, 115)
CREAM = (250, 243, 235)
PURPLE = ROSE  # обратная совместимость имени переменной по коду ниже


def _setup_pdf() -> FPDF:
    pdf = FPDF()
    pdf.add_font("DejaVu", "", FONT)
    pdf.add_font("DejaVu", "B", FONT_BOLD)
    pdf.set_auto_page_break(auto=True, margin=20)
    return pdf


def _cover(pdf: FPDF, title: str, subtitle: str, name: str, birthdate: str):
    pdf.add_page()
    pdf.set_fill_color(*ROSE)
    pdf.rect(0, 0, 210, 297, "F")
    pdf.set_fill_color(*GOLD)
    pdf.rect(0, 70, 210, 1, "F")
    pdf.rect(0, 226, 210, 1, "F")
    pdf.set_text_color(255, 255, 255)
    pdf.set_y(90)
    pdf.set_font("DejaVu", "B", 26)
    pdf.multi_cell(0, 12, title, align="C")
    pdf.ln(4)
    pdf.set_font("DejaVu", "", 14)
    pdf.multi_cell(0, 8, subtitle, align="C")
    pdf.ln(20)
    pdf.set_font("DejaVu", "B", 16)
    pdf.cell(0, 8, name, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 12)
    pdf.cell(0, 8, f"Дата рождения: {birthdate}", align="C")


def _section_header(pdf: FPDF, number: str, title: str, subtitle: str):
    pdf.set_fill_color(*CREAM)
    pdf.rect(0, 0, 210, 297, "F")
    pdf.set_fill_color(*ROSE)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("DejaVu", "B", 13)
    pdf.cell(0, 10, f"  {number}", fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)
    pdf.set_text_color(*DARK)
    pdf.set_font("DejaVu", "B", 14)
    pdf.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*GRAY)
    pdf.set_font("DejaVu", "", 10)
    pdf.cell(0, 6, subtitle, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)


def _arcana_block(pdf: FPDF, arcana_num: int, text: str):
    pdf.set_text_color(*GOLD)
    pdf.set_font("DejaVu", "B", 12)
    pdf.cell(0, 7, f"Аркан {arcana_num} · {get_arcana_name(arcana_num)}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*DARK)
    pdf.set_font("DejaVu", "", 11)
    pdf.multi_cell(0, 6, text)
    pdf.ln(4)


def generate_free_pdf(name: str, day: int, month: int, year: int, output_path: str):
    birthdate = f"{day:02d}.{month:02d}.{year}"
    result = calculate_matrix(day, month, year)
    pdf = _setup_pdf()

    _cover(pdf, "МАТРИЦА СУДЬБЫ", "Мини-разбор: кто ты по своей сути", name, birthdate)

    pdf.add_page()
    pdf.set_text_color(*DARK)
    _section_header(pdf, "01", "Точка Личности", "Кто ты в своей основе")
    _arcana_block(pdf, result["A_day"], get_arcana_text("A_day", result["A_day"]))

    pdf.ln(6)
    pdf.set_draw_color(*GOLD)
    pdf.line(20, pdf.get_y(), 190, pdf.get_y())
    pdf.ln(8)

    pdf.set_font("DejaVu", "B", 13)
    pdf.set_text_color(*ROSE)
    pdf.multi_cell(0, 7, "Это лишь первая точка твоей Матрицы Судьбы.")
    pdf.ln(2)
    pdf.set_font("DejaVu", "", 11)
    pdf.set_text_color(*DARK)
    pdf.multi_cell(0, 6,
        "В полной матрице ещё 11 ключевых точек: твоё предназначение, "
        "денежный канал, модель отношений и кармический хвост — то, что "
        "тянется из прошлого и мешает двигаться вперёд.\n\n"
        "Хочешь узнать свой полный разбор — напиши мне в директ "
        "или оформи полный отчёт прямо в этом чате."
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pdf.output(output_path)
    return output_path


def generate_full_pdf(name: str, day: int, month: int, year: int, output_path: str):
    birthdate = f"{day:02d}.{month:02d}.{year}"
    result = calculate_matrix(day, month, year)
    pdf = _setup_pdf()

    _cover(pdf, "МАТРИЦА СУДЬБЫ", "Полный персональный разбор · 12 ключевых точек", name, birthdate)

    for idx, (key, title, subtitle) in enumerate(POSITIONS, start=1):
        pdf.add_page()
        pdf.set_text_color(*DARK)
        _section_header(pdf, f"{idx:02d}", title, subtitle)
        arcana_num = result[key]
        _arcana_block(pdf, arcana_num, get_arcana_text(key, arcana_num))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pdf.output(output_path)
    return output_path


if __name__ == "__main__":
    generate_free_pdf("Тестовый пример", 14, 3, 1991, "/home/user/matrix_product/output/free_sample.pdf")
    generate_full_pdf("Тестовый пример", 14, 3, 1991, "/home/user/matrix_product/output/full_sample.pdf")
    print("PDF созданы")
