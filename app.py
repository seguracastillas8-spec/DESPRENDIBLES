from flask import Flask, render_template, request, redirect, session
import os

from auth import login_required
from ocr.reader import leer_archivo
from ocr.extractors import extraer_datos
from logic.calculations import calcular_cde

app = Flask(__name__)
app.secret_key = "clave-super-privada"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["user"] == "admin" and request.form["password"] == "1234":
            session["user"] = "admin"
            return redirect("/upload")
    return render_template("login.html")

@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        archivo = request.files["file"]
        ruta = os.path.join(UPLOAD_FOLDER, archivo.filename)
        archivo.save(ruta)

        texto = leer_archivo(ruta)
        datos = extraer_datos(texto)
        resultado = calcular_cde(datos)

        return render_template("result.html", **resultado)

    return render_template("upload.html")

app.run(debug=True)
