# data/

Datasets pequeños de **respaldo** para trabajar sin conexión o cuando una API falle en clase.

Regla del curso: los notebooks descargan todo **por API** (reproducibilidad). Fuentes:

| Fuente | Qué usamos | Acceso |
|---|---|---|
| BCRPData (BCRP) | Tipo de cambio, IGBVL/S&P BVL, tasas, inflación | `utils/bcrp.py` |
| FRED (FED St. Louis) | Treasuries, fed funds, CPI | `utils/fred.py` |
| Yahoo Finance | Acciones, ETF, futuros (cobre HG=F) | `yfinance` |
| Biblioteca de Kenneth French | Factores Fama-French (3 y 5), *momentum*, mercados emergentes | `utils/french.py` |
| SBS / MEF | Curvas soberanas del Perú | descarga manual  CSV aquí |

Los CSV de respaldo se nombran `fuente_serie_frecuencia.csv` (p. ej. `bcrp_tc_mensual.csv`).
