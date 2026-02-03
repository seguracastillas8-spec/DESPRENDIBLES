from logic.pagadurias import PAGADURIAS

def calcular_cde(datos):
    pension = datos["pension"]
    salud = datos["salud"]
    deducciones = datos["deducciones"]
    pagaduria = datos["pagaduria"]

    margen, sector = PAGADURIAS.get(pagaduria, (0, "DESCONOCIDO"))

    ingreso_neto = pension - salud
    resultado = ingreso_neto / 2
    cde = resultado - margen - deducciones

    return {
        "pagaduria": pagaduria,
        "sector": sector,
        "pension": pension,
        "salud": salud,
        "ingreso_neto": ingreso_neto,
        "resultado": resultado,
        "margen": margen,
        "cde": cde
    }
