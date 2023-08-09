import json
import os

from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from src.handlers import handle_analyze, handle_upload, ANALYSES_FOLDER, UPLOAD_FOLDER

app = Flask(__name__)
app.secret_key = b"6b3c3553ae7c43e5a6d4bf069b496ed6e29db4b94044be78b3bdd95f2dd75a5d"


@app.route("/")
def index():
    existing_files = get_files()
    return render_template("index.html", existing_files=existing_files)


def get_files():
    return [
        f
        for f in os.listdir(UPLOAD_FOLDER)
        if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))
    ]


@app.post("/upload")
def upload_file():
    if "upload_file" not in request.files:
        flash("File is required.")
        return redirect(url_for("index"))

    delimiter_str = request.form["delimiter"]

    if not delimiter_str:
        flash("Please select delimiter")
        return redirect(url_for("index"))

    delimiter = get_delimiter(delimiter_str)

    f = request.files["upload_file"]
    filename = secure_filename(f.filename)
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    f.save(save_path)

    csv_cols = handle_upload(save_path, delimiter)

    return render_template(
        "column_selector.html", cols=csv_cols, filename=filename, delimiter=delimiter
    )


@app.post("/analyze")
def analyze():

    column = request.form.get("col")
    filename = request.form.get("filename")
    delimiter = request.form.get("delimiter")

    if not column or not filename or not delimiter:
        flash("An unexpected error occurred.")
        return redirect(url_for("index"))

    count_tuples, errors = handle_analyze(filename, column, delimiter)

    return render_template(
        "analysis.html",
        filename=filename,
        count_tuples=count_tuples,
        errors=errors,
    )


@app.get("/view/<filename>")
def view(filename):
    analysis_path = os.path.join(ANALYSES_FOLDER, filename + ".json")
    with open(analysis_path, "rt") as fin:
        analysis = json.load(fin)

    count_tuples = analysis["count_tuples"]
    errors = analysis["errors"]

    return render_template(
        "analysis.html",
        filename=filename,
        count_tuples=count_tuples,
        errors=errors,
    )


def get_delimiter(delimiter_str: str) -> str:
    if delimiter_str == "comma":
        return ","

    if delimiter_str == "tab":
        return "\t"

    raise ValueError("Unsupported delimiter.")
