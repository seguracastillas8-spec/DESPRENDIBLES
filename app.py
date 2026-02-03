from flask import Flask, render_template, request, redirect, session
from users import USERS
from pagadurias import PAGADURIAS
import os
import re

# =========================
# CONFIGURACIÓN BÁSICA
# =========================

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "cde_seguro_2026")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =========================
# FUNCIONES OCR (CARGA DIFERIDA)
# =========================

def extract_text(file_path: str) -> str:
    return ""

    """
    Extrae texto desde PDF o imagen (PNG/JPG)
    usando OCR solo cuando se necesita.
    """
    if file_path.lower().endswith(".pdf"):
        import pdfplumber
        texto = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                texto += page.extract_text() or ""
        return texto
    else:
        import pytesseract
        from PIL import Image
        img = Image.open(file_path)
        return pytesseract.image_to_string(img)

def parse_data(text: str):
    """
    Extrae:
    - Valor pensión
    - Descuento salud (12%)
    - Pagaduría
    """
    # Buscar número grande (valor pensión)
    match = re.search(r"([\d\.]{6,})", text)
    pension = int(match.group(1).replace(".", "")) if match else 0

    salud = int(pension * 0.12)

    pagaduria = next(
        (p for p in PAGADURIAS.keys() if p in text.upper()),
        "NO IDENTIFICADA"
    )

    return pension, salud, pagaduria

# =========================
# RUTAS
# =========================

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("user")
        clave = request.form.get("password")

        if USERS.get(usuario) == clave:
            session["user"] = usuario
            return redirect("/dashboard")

    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/")

    data = None

    if request.method == "POST":
        archivo = request.files.get("file")

        if archivo and archivo.filename:
            ruta = os.path.join(UPLOAD_FOLDER, archivo.filename)
            archivo.save(ruta)

            texto = extract_text(ruta)
            pension, salud, pagaduria = parse_data(texto)

            info_pagaduria = PAGADURIAS.get(pagaduria, {})
            margen = info_pagaduria.get("margen", 0)
            sector = info_pagaduria.get("sector", "NO DEFINIDO")

            ingreso_neto = pension - salud
            resultado = ingreso_neto / 2
            cde = resultado - margen

            data = {
                "pagaduria": pagaduria,
                "pension": pension,
                "salud": salud,
                "ingreso_neto": ingreso_neto,
                "resultado": resultado,
                "margen": margen,
                "cde": cde,
                "sector": sector
            }

    return render_template("dashboard.html", data=data)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
