"""
metricas.py — Cálculo del Índice de Selección Adversa (ISA)

Decisiones metodológicas documentadas:
-----------------------------------------
1. PERÍODO BASE: enero–diciembre 2023 (pre-shock Milei).
   Justificación: comportamiento estructural del mercado en condiciones
   no perturbadas. Correlación Pearson entre componentes en base: -0.89.

2. NORMALIZACIÓN: z-score con parámetros fijos del período base.
   Permite incorporar datos futuros sin recalibrar la escala histórica.
   Parámetros calculados en script diagnóstico (Evaluación de Condiciones.py).

3. SIGNO de pct_protocolo21: NEGATIVO.
   Justificación: mayor participación Protocolo 21 rejuvenece el parque
   circulante, reduciendo antigüedad media. El signo negativo alinea ambos
   componentes en la misma dirección de deterioro de mercado.

4. PONDERACIÓN: 50/50 (base). Variantes 70/30 y 30/70 para análisis
   de sensibilidad en Notebook 03.

5. ARQUITECTURA MULTI-RÉGIMEN: el ISA es sensible a rupturas estructurales
   (cambios de régimen de importaciones, política cambiaria, crisis sistémicas).
   Ante una nueva ruptura, se agrega un ítem a REGIMENES sin modificar los
   parámetros históricos. La serie histórica permanece intacta.

Limitaciones activas:
-----------------------------------------
- pct_protocolo21 en usados tiene interpretación dual post-2024:
  proxy de opacidad informacional (régimen cerrado) vs. proxy de política
  de importaciones (régimen abierto). El modelo ADL en Notebook 03 debe
  controlar por dummy de régimen.
- El ISA mide transacciones completadas, no intenciones frustradas
  (punto ciego de Akerlof). Es proxy del deterioro observable, no medición
  directa de calidad oculta.
"""

import pandas as pd
from typing import Optional

# ---------------------------------------------------------------------------
# REGÍMENES — lista extensible
# Agregar nuevos regímenes sin modificar los existentes.
# ---------------------------------------------------------------------------

REGIMENES = [
    {
        "id":             "2023_base",
        "label":          "Régimen cerrado — pre-shock Milei",
        "descripcion":    (
            "Mercado con importaciones restringidas. pct_protocolo21 refleja "
            "principalmente opacidad informacional, no política de apertura. "
            "Correlación Pearson antiguedad/protocolo21: -0.89."
        ),
        "vigente_desde":  "2023-01",
        "vigente_hasta":  "2023-12",
        "params": {
            "antiguedad_media": {"media": 14.2872, "desvio": 0.2009},
            "pct_protocolo21":  {"media": 40.1565, "desvio": 0.9204},
        },
    },
    # --- Ejemplo de cómo agregar un nuevo régimen en 2027 ---
    # {
    #     "id":            "2027_base",
    #     "label":         "Régimen post-X — descripción del contexto",
    #     "descripcion":   "...",
    #     "vigente_desde": "2027-01",
    #     "vigente_hasta": "2027-12",
    #     "params": {
    #         "antiguedad_media": {"media": X.XXXX, "desvio": X.XXXX},
    #         "pct_protocolo21":  {"media": XX.XXXX, "desvio": X.XXXX},
    #     },
    # },
]


# ---------------------------------------------------------------------------
# FUNCIÓN AUXILIAR — selección de régimen
# ---------------------------------------------------------------------------

def obtener_regimen(regimen_id: str = "2023_base") -> dict:
    """
    Retorna el diccionario de parámetros del régimen solicitado.

    Parámetros
    ----------
    regimen_id : str
        ID del régimen definido en REGIMENES. Default: '2023_base'.

    Retorna
    -------
    dict
        Diccionario completo del régimen, incluyendo params.

    Raises
    ------
    ValueError
        Si el regimen_id no existe en REGIMENES.
    """
    for r in REGIMENES:
        if r["id"] == regimen_id:
            return r

    ids_disponibles = [r["id"] for r in REGIMENES]
    raise ValueError(
        f"Régimen '{regimen_id}' no encontrado. "
        f"Disponibles: {ids_disponibles}"
    )


# ---------------------------------------------------------------------------
# FUNCIÓN PRINCIPAL — cálculo del ISA
# ---------------------------------------------------------------------------

def calcular_isa(
    serie: pd.DataFrame,
    regimen_id: str = "2023_base",
) -> pd.DataFrame:
    """
    Calcula el ISA mensual sobre una serie temporal de usados.

    Parámetros
    ----------
    serie : pd.DataFrame
        Serie temporal con columnas 'antiguedad_media' y 'pct_protocolo21'.
        Generada por pipeline.construir_serie('usados').
    regimen_id : str
        ID del régimen base para normalización. Default: '2023_base'.
        Para comparar regímenes, llamar dos veces con distintos IDs.

    Retorna
    -------
    pd.DataFrame
        Serie original con columnas adicionales:
        - z_antiguedad  : z-score de antigüedad (+ = más deterioro)
        - z_protocolo21 : z-score de protocolo21, signo invertido (+ = más deterioro)
        - ISA           : índice compuesto 50/50
        - ISA_70_30     : sensibilidad — más peso a antigüedad
        - ISA_30_70     : sensibilidad — más peso a protocolo21
        - regimen_id    : identificador del régimen usado (trazabilidad)
    """
    regimen = obtener_regimen(regimen_id)
    params  = regimen["params"]

    df = serie.copy()

    # Z-score de antigüedad — signo positivo: más años = más deterioro
    df["z_antiguedad"] = (
        (df["antiguedad_media"] - params["antiguedad_media"]["media"])
        / params["antiguedad_media"]["desvio"]
    )

    # Z-score de protocolo21 — signo NEGATIVO:
    # más protocolo21 = parque más joven = menos deterioro
    df["z_protocolo21"] = -(
        (df["pct_protocolo21"] - params["pct_protocolo21"]["media"])
        / params["pct_protocolo21"]["desvio"]
    )

    # ISA principal 50/50
    df["ISA"] = (
        df["z_antiguedad"] * 0.5 +
        df["z_protocolo21"] * 0.5
    )

    # Variantes para análisis de sensibilidad en Notebook 03
    df["ISA_70_30"] = df["z_antiguedad"] * 0.7 + df["z_protocolo21"] * 0.3
    df["ISA_30_70"] = df["z_antiguedad"] * 0.3 + df["z_protocolo21"] * 0.7

    # Trazabilidad — qué régimen se usó para calcular este ISA
    df["regimen_id"] = regimen_id

    return df