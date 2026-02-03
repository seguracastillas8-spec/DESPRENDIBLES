from flask import Flask, render_template, request, redirect, session
from users import USERS
from pagadurias import PAGADURIAS
import pytesseract, pdfplumber, re, os
from PIL import Image

app = Flask(__name__)
import os
app.secret_key = os.environ.get("SECRET_KEY")
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extract_text(file_path):
    if file_path.endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            return " ".join(page.extract_text() or "" for page in pdf.pages)
    else:
        img = Image.open(file_path)
        return pytesseract.image_to_string(img)

def parse_data(text):
    pension = int(re.search(r"\$?\s?([\d\.]+)", text).group(1).replace(".", ""))
    salud = int(pension * 0.12)
    pagaduria = next((p for p in PAGADURIAS if p in text.upper()), "NO IDENTIFICADA")
    return pension, salud, pagaduria

@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        if USERS.get(request.form["user"]) == request.form["password"]:
            session["user"] = request.form["user"]
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/dashboard", methods=["GET","POST"])
def dashboard():
    if "user" not in session:
        return redirect("/")
    data = None
    if request.method == "POST":
        f = request.files["file"]
        path = os.path.join(UPLOAD_FOLDER, f.filename)
        f.save(path)
        text = extract_text(path)
        pension, salud, pagaduria = parse_data(text)
        margen = PAGADURIAS.get(pagaduria, {}).get("margen", 0)
        sector = PAGADURIAS.get(pagaduria, {}).get("sector", "")
        ingreso = pension - salud
        cde = (ingreso / 2) - margen
        data = [pagaduria, pension, salud, ingreso, cde, sector]
    return render_template("dashboard.html", data=data)

