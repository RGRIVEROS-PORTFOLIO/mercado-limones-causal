"""
visualizacion.py — Funciones de graficado para mercado-limones-causal

Principio de diseño:
    Cada función recibe datos como argumento y guarda la figura
    en la ruta indicada. El notebook llama estas funciones —
    no implementa lógica visual propia.

Uso típico en Notebook 03:
    from visualizacion import graficar_series_temporales
    graficar_series_temporales(serie_isa, serie_0km, output_path)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path


# ---------------------------------------------------------------------------
# CONFIGURACIÓN VISUAL GLOBAL
# ---------------------------------------------------------------------------

COLORES = {
    "isa":        "#c0392b",
    "cero_km":    "#27ae60",
    "neutro":     "#7f8c8d",
    "shock":      "#e67e22",
    "deterioro":  "#c0392b",
    "mejora":     "#2980b9",
    "isa_70_30":  "#8e44ad",
    "isa_30_70":  "#16a085",
}

ESTILO = {
    "figsize_triple": (14, 10),
    "figsize_doble":  (14, 7),
    "figsize_simple": (12, 5),
    "dpi":            150,
    "grid_alpha":     0.3,
    "fill_alpha":     0.15,
}


def _formato_eje_fecha(ax):
    """Aplica formato estándar al eje x de fechas."""
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")


def _guardar(fig, output_path: Path, nombre: str):
    """Guarda figura y confirma por consola."""
    output_path.mkdir(parents=True, exist_ok=True)
    ruta = output_path / nombre
    fig.savefig(ruta, dpi=ESTILO["dpi"], bbox_inches="tight")
    plt.close(fig)
    print(f"✅ Figura guardada: {ruta}")


# ---------------------------------------------------------------------------
# FUNCIÓN 1 — Series temporales
# ---------------------------------------------------------------------------

def graficar_series_temporales(
    serie_isa: pd.DataFrame,
    serie_0km: pd.DataFrame,
    output_path: Path,
) -> None:
    """
    Panel triple: ISA, Volumen 0km, y superposición normalizada.

    Parámetros
    ----------
    serie_isa   : DataFrame con columnas 'fecha', 'ISA'
    serie_0km   : DataFrame con columnas 'fecha', 'total'
    output_path : directorio donde guardar la figura
    """
    fig, axes = plt.subplots(3, 1,
                             figsize=ESTILO["figsize_triple"],
                             sharex=True)
    fig.suptitle(
        "Mercado de Limones Argentino — Series temporales\n"
        "ISA (Índice de Selección Adversa) y Volumen 0km",
        fontsize=13, fontweight="bold"
    )

    shock = pd.Timestamp("2024-01")
    apertura = pd.Timestamp("2025-01")

    # --- Panel 1: ISA ---
    ax = axes[0]
    ax.plot(serie_isa["fecha"], serie_isa["ISA"],
            color=COLORES["isa"], linewidth=2, label="ISA (50/50)")
    ax.fill_between(serie_isa["fecha"], serie_isa["ISA"], 0,
                    where=serie_isa["ISA"] > 0,
                    alpha=ESTILO["fill_alpha"],
                    color=COLORES["deterioro"], label="Zona deterioro")
    ax.fill_between(serie_isa["fecha"], serie_isa["ISA"], 0,
                    where=serie_isa["ISA"] < 0,
                    alpha=ESTILO["fill_alpha"],
                    color=COLORES["mejora"], label="Zona mejora")
    ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
    ax.axvline(shock, color=COLORES["shock"],
               linewidth=1.5, linestyle=":", label="Shock Milei (ene-2024)")
    ax.axvline(apertura, color=COLORES["neutro"],
               linewidth=1.5, linestyle=":", label="Apertura consolidada (2025)")
    ax.set_ylabel("ISA (z-score)")
    ax.legend(fontsize=8, loc="upper right")
    ax.set_title("ISA — Índice de Selección Adversa", fontsize=10)
    ax.grid(True, alpha=ESTILO["grid_alpha"])

    # --- Panel 2: Volumen 0km ---
    ax = axes[1]
    ax.bar(serie_0km["fecha"], serie_0km["total"] / 1000,
           color=COLORES["cero_km"], alpha=0.7,
           width=20, label="Inscripciones 0km (miles)")
    ax.axvline(shock, color=COLORES["shock"],
               linewidth=1.5, linestyle=":", label="Shock Milei")
    ax.axvline(apertura, color=COLORES["neutro"],
               linewidth=1.5, linestyle=":")
    ax.set_ylabel("Miles de unidades")
    ax.legend(fontsize=8, loc="upper right")
    ax.set_title("Volumen 0km — Variable predictora", fontsize=10)
    ax.grid(True, alpha=ESTILO["grid_alpha"])

    # --- Panel 3: Superposición normalizada ---
    ax = axes[2]
    vol_norm = ((serie_0km["total"] - serie_0km["total"].mean())
                / serie_0km["total"].std())
    ax.plot(serie_isa["fecha"], serie_isa["ISA"],
            color=COLORES["isa"], linewidth=2, label="ISA")
    ax.plot(serie_0km["fecha"], vol_norm,
            color=COLORES["cero_km"], linewidth=2,
            linestyle="--", label="0km (normalizado)")
    ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
    ax.axvline(shock, color=COLORES["shock"],
               linewidth=1.5, linestyle=":", label="Shock Milei")
    ax.axvline(apertura, color=COLORES["neutro"],
               linewidth=1.5, linestyle=":")
    ax.set_ylabel("Z-score")
    ax.legend(fontsize=8, loc="upper right")
    ax.set_title("Superposición — ¿El 0km precede al ISA?", fontsize=10)
    ax.grid(True, alpha=ESTILO["grid_alpha"])
    _formato_eje_fecha(ax)

    plt.tight_layout()
    _guardar(fig, output_path, "01_series_temporales.png")


# ---------------------------------------------------------------------------
# FUNCIÓN 2 — Función de Correlación Cruzada (CCF)
# ---------------------------------------------------------------------------

def graficar_ccf(
    serie_isa: pd.DataFrame,
    serie_0km: pd.DataFrame,
    output_path: Path,
    max_lags: int = 12,
) -> None:
    """
    Correlación cruzada entre volumen 0km e ISA con distintos rezagos.
    Muestra en qué lag el 0km tiene mayor correlación con el ISA futuro.

    Parámetros
    ----------
    serie_isa  : DataFrame con columna 'ISA'
    serie_0km  : DataFrame con columna 'total'
    output_path: directorio donde guardar la figura
    max_lags   : número máximo de rezagos a evaluar (default: 12)
    """
    isa  = serie_isa["ISA"].values
    vol  = serie_0km["total"].values

    # Normalizar antes de calcular CCF
    isa_z = (isa  - isa.mean())  / isa.std()
    vol_z = (vol  - vol.mean())  / vol.std()

    correlaciones = [
        np.corrcoef(vol_z[:-lag], isa_z[lag:])[0, 1]
        if lag > 0
        else np.corrcoef(vol_z, isa_z)[0, 1]
        for lag in range(max_lags + 1)
    ]

    # Banda de significancia ±1.96/√n
    n   = len(isa)
    banda = 1.96 / np.sqrt(n)

    fig, ax = plt.subplots(figsize=ESTILO["figsize_simple"])
    lags = range(max_lags + 1)

    colores_barras = [
        COLORES["isa"] if abs(c) > banda else COLORES["neutro"]
        for c in correlaciones
    ]
    ax.bar(lags, correlaciones, color=colores_barras, alpha=0.8)
    ax.axhline( banda, color="black", linewidth=1, linestyle="--",
                label=f"Significancia ±{banda:.2f} (95%)")
    ax.axhline(-banda, color="black", linewidth=1, linestyle="--")
    ax.axhline(0, color="black", linewidth=0.5)

    ax.set_xlabel("Rezago (meses) — 0km adelantado respecto al ISA")
    ax.set_ylabel("Correlación de Pearson")
    ax.set_title(
        "Función de Correlación Cruzada (CCF)\n"
        "¿En cuántos meses el volumen 0km anticipa el ISA?",
        fontsize=11, fontweight="bold"
    )
    ax.legend(fontsize=9)
    ax.grid(True, alpha=ESTILO["grid_alpha"])
    ax.set_xticks(list(lags))

    plt.tight_layout()
    _guardar(fig, output_path, "02_ccf.png")


# ---------------------------------------------------------------------------
# FUNCIÓN 3 — Análisis de sensibilidad del ISA
# ---------------------------------------------------------------------------

def graficar_sensibilidad_isa(
    serie_isa: pd.DataFrame,
    output_path: Path,
) -> None:
    """
    Superpone ISA, ISA_70_30 e ISA_30_70.
    Si las tres curvas son similares, la ponderación no es determinante.

    Parámetros
    ----------
    serie_isa  : DataFrame con columnas 'fecha', 'ISA', 'ISA_70_30', 'ISA_30_70'
    output_path: directorio donde guardar la figura
    """
    fig, ax = plt.subplots(figsize=ESTILO["figsize_simple"])

    ax.plot(serie_isa["fecha"], serie_isa["ISA"],
            color=COLORES["isa"], linewidth=2.5,
            label="ISA 50/50 (base)")
    ax.plot(serie_isa["fecha"], serie_isa["ISA_70_30"],
            color=COLORES["isa_70_30"], linewidth=1.5,
            linestyle="--", label="ISA 70/30 (más peso antigüedad)")
    ax.plot(serie_isa["fecha"], serie_isa["ISA_30_70"],
            color=COLORES["isa_30_70"], linewidth=1.5,
            linestyle=":", label="ISA 30/70 (más peso protocolo21)")

    ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
    ax.axvline(pd.Timestamp("2024-01"), color=COLORES["shock"],
               linewidth=1.5, linestyle=":", label="Shock Milei")
    ax.set_ylabel("ISA (z-score)")
    ax.set_title(
        "Análisis de Sensibilidad del ISA\n"
        "¿Cambian las conclusiones según la ponderación?",
        fontsize=11, fontweight="bold"
    )
    ax.legend(fontsize=9)
    ax.grid(True, alpha=ESTILO["grid_alpha"])
    _formato_eje_fecha(ax)

    plt.tight_layout()
    _guardar(fig, output_path, "03_sensibilidad_isa.png")


# ---------------------------------------------------------------------------
# FUNCIÓN 4 — Diagnóstico de residuos del modelo ADL
# ---------------------------------------------------------------------------

def graficar_residuos_adl(
    residuos: pd.Series,
    output_path: Path,
) -> None:
    """
    Panel de diagnóstico de residuos del modelo ADL.
    Verifica: normalidad, homocedasticidad, ausencia de autocorrelación.

    Parámetros
    ----------
    residuos   : Serie de residuos del modelo ajustado
    output_path: directorio donde guardar la figura
    """
    from scipy import stats

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    fig.suptitle("Diagnóstico de Residuos — Modelo ADL",
                 fontsize=12, fontweight="bold")

    # --- Residuos en el tiempo ---
    ax = axes[0]
    ax.plot(residuos.values, color=COLORES["isa"],
            linewidth=1.5, marker="o", markersize=3)
    ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
    ax.set_title("Residuos en el tiempo")
    ax.set_xlabel("Observación")
    ax.set_ylabel("Residuo")
    ax.grid(True, alpha=ESTILO["grid_alpha"])

    # --- Histograma con curva normal ---
    ax = axes[1]
    ax.hist(residuos, bins=10, color=COLORES["cero_km"],
            alpha=0.7, edgecolor="white", density=True)
    x = np.linspace(residuos.min(), residuos.max(), 100)
    ax.plot(x, stats.norm.pdf(x, residuos.mean(), residuos.std()),
            color="black", linewidth=1.5, label="Normal teórica")
    ax.set_title("Distribución de residuos")
    ax.set_xlabel("Residuo")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=ESTILO["grid_alpha"])

    # --- Q-Q Plot ---
    ax = axes[2]
    stats.probplot(residuos, dist="norm", plot=ax)
    ax.set_title("Q-Q Plot (normalidad)")
    ax.grid(True, alpha=ESTILO["grid_alpha"])

    plt.tight_layout()
    _guardar(fig, output_path, "04_residuos_adl.png")