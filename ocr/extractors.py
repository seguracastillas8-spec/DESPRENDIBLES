import re
from logic.pagadurias import PAGADURIAS

def buscar_valor(clave, texto):
    match = re.search(rf"{clave}.*?([\d\.,]+)", texto, re.IGNORECASE)
    return float(match.group(1).replace(".", "").replace(",", ".")) if match else 0

def buscar_pagaduria(texto):
    for p in PAGADURIAS:
        if p in texto.upper():
            return p
    return "NO IDENTIFICADA"

def extraer_datos(texto):
    return {
        "cliente": "CLIENTE NO IDENTIFICADO",
        "pagaduria": buscar_pagaduria(texto),
        "pension": buscar_valor("pension", texto),
        "salud": buscar_valor("salud", texto),
        "deducciones": buscar_valor("deducciones", texto)
    }
