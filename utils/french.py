"""Descarga de factores de la biblioteca de datos de Kenneth French (Dartmouth), sin API key.

Los archivos son CSV comprimidos con un encabezado de texto, un bloque mensual y,
al final, un bloque anual. Esta función devuelve solo el bloque mensual, en decimales.

Ejemplo
-------
>>> from utils.french import get_factores
>>> ff3 = get_factores()                 # Mkt-RF, SMB, HML y RF (Estados Unidos)
>>> mom = get_factores("momentum")       # factor momentum (WML)
"""
from __future__ import annotations

import io
import zipfile

import pandas as pd
import requests

BASE = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp"

ARCHIVOS = {
    "ff3": "F-F_Research_Data_Factors_CSV.zip",
    "ff5": "F-F_Research_Data_5_Factors_2x3_CSV.zip",
    "momentum": "F-F_Momentum_Factor_CSV.zip",
    "emergentes": "Emerging_5_Factors_CSV.zip",
}


def get_factores(cual: str = "ff3", inicio: str | None = None, fin: str | None = None) -> pd.DataFrame:
    """Factores mensuales de Ken French como DataFrame en decimales, con índice mensual (PeriodIndex).

    Parameters
    ----------
    cual : str
        "ff3" (Mkt-RF, SMB, HML, RF), "ff5" (agrega RMW y CMA), "momentum" (WML)
        o "emergentes" (5 factores de mercados emergentes). También acepta el nombre
        exacto de un archivo .zip de la biblioteca.
    inicio, fin : str, opcional
        Meses "AAAA-MM" para recortar la muestra.
    """
    archivo = ARCHIVOS.get(cual, cual)
    r = requests.get(f"{BASE}/{archivo}", timeout=60, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        texto = z.read(z.namelist()[0]).decode("latin-1")

    filas, columnas = [], None
    for linea in texto.splitlines():
        partes = [p.strip() for p in linea.split(",")]
        if columnas is None:
            if len(partes) > 1 and partes[0] == "" and all(partes[1:]):
                columnas = partes[1:]                      # la fila de nombres empieza con una coma
            continue
        if len(partes[0]) == 6 and partes[0].isdigit():    # AAAAMM: bloque mensual
            filas.append(partes[: len(columnas) + 1])
        elif filas:
            break                                          # termino el bloque mensual
    if not filas:
        raise ValueError(f"No se pudo leer el bloque mensual de {archivo}")

    df = pd.DataFrame(filas, columns=["mes", *columnas]).set_index("mes")
    df.index = pd.PeriodIndex(pd.to_datetime(df.index, format="%Y%m"), freq="M")
    df = df.apply(pd.to_numeric, errors="coerce")
    df = df.where(df > -99).dropna() / 100                 # -99.99 es el codigo de dato faltante
    df.columns = [c.replace(" ", "") for c in df.columns]
    if inicio:
        df = df.loc[inicio:]
    if fin:
        df = df.loc[:fin]
    return df
