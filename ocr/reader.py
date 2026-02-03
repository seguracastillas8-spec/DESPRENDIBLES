import os
import pdfplumber
import pytesseract
import cv2

def ocr_imagen(ruta):
    img = cv2.imread(ruta)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
    return pytesseract.image_to_string(gray, lang="spa")

def leer_pdf(ruta):
    texto = ""
    with pdfplumber.open(ruta) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                texto += page.extract_text()
            else:
                img = page.to_image(resolution=300).original
                texto += pytesseract.image_to_string(img, lang="spa")
    return texto

def leer_archivo(ruta):
    ext = os.path.splitext(ruta)[1].lower()
    if ext == ".pdf":
        return leer_pdf(ruta)
    if ext in [".png", ".jpg", ".jpeg"]:
        return ocr_imagen(ruta)
    raise ValueError("Formato no soportado")
