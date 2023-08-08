import tempfile

from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = b"6b3c3553ae7c43e5a6d4bf069b496ed6e29db4b94044be78b3bdd95f2dd75a5d"


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/upload")
def upload_file():
    if "file" not in request.files:
        flash("File is required.")
        return redirect(url_for("index"))

    f = request.files["file"]
    f.save(f"./{secure_filename(f.filename)}")
