"""Калькулятор Матрицы Судьбы (методика Н. Ладини) + генератор PDF-отчётов."""
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "arcana_texts.json"), encoding="utf-8") as f:
    ARCANA_TEXTS = {int(k): v for k, v in json.load(f).items()}

with open(os.path.join(BASE_DIR, "positions.json"), encoding="utf-8") as f:
    POSITIONS = json.load(f)  # list of [key, title, subtitle]


def reduce22(n: int) -> int:
    while n > 22:
        n = sum(int(d) for d in str(n))
    return n


def calculate_matrix(day: int, month: int, year: int) -> dict:
    A = reduce22(day)
    B = reduce22(month)
    C = reduce22(sum(int(d) for d in str(year)))
    D = reduce22(A + B + C)
    center = reduce22(A + B + C + D)

    money_entry = reduce22(C + center)
    money_channel = reduce22(money_entry + D)

    rel_entry = reduce22(D + center)
    rel_channel = reduce22(rel_entry + D)

    duh_line = reduce22(B + D)
    mat_line = reduce22(A + C)
    personal_fate = reduce22(duh_line + mat_line)

    return {
        "A_day": A, "B_month": B, "C_year": C, "D_karma": D,
        "center": center,
        "money_entry": money_entry, "money_channel": money_channel,
        "rel_entry": rel_entry, "rel_channel": rel_channel,
        "duh_line": duh_line, "mat_line": mat_line,
        "personal_fate": personal_fate,
    }


def get_arcana_text(position_key: str, arcana_number: int) -> str:
    return ARCANA_TEXTS[arcana_number][position_key]


def get_arcana_name(arcana_number: int) -> str:
    return ARCANA_TEXTS[arcana_number]["name"]


if __name__ == "__main__":
    result = calculate_matrix(14, 3, 1991)
    for key, value in result.items():
        print(f"{key} = {value} ({get_arcana_name(value)})")
