"""
Веб-сервис для генерации PDF-отчётов Матрицы Судьбы.
Разверните на Render/Railway/PythonAnywhere — SaleBot будет дёргать этот API.

Эндпоинты:
  GET /generate?type=free&day=14&month=3&year=1991&name=Анна
  GET /generate?type=full&day=14&month=3&year=1991&name=Анна

Возвращает JSON: {"pdf_url": "https://ваш-домен/files/xxxx.pdf"}
"""
import os
import uuid
from flask import Flask, request, jsonify, send_from_directory

from pdf_generator import generate_free_pdf, generate_full_pdf

app = Flask(__name__)
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generated")
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.route("/generate")
def generate():
    report_type = request.args.get("type", "free")
    name = request.args.get("name", "Друг")
    try:
        day = int(request.args.get("day"))
        month = int(request.args.get("month"))
        year = int(request.args.get("year"))
    except (TypeError, ValueError):
        return jsonify({"error": "Нужны числовые параметры day, month, year"}), 400

    filename = f"{uuid.uuid4().hex}.pdf"
    output_path = os.path.join(OUTPUT_DIR, filename)

    if report_type == "full":
        generate_full_pdf(name, day, month, year, output_path)
    else:
        generate_free_pdf(name, day, month, year, output_path)

    pdf_url = request.host_url.rstrip("/") + f"/files/{filename}"
    return jsonify({"pdf_url": pdf_url})


@app.route("/files/<path:filename>")
def serve_file(filename):
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=False)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
