"""
pipeline.py — ETL mensual para transferencias y 0km DNRPA

Flujo por archivo:
    CSV crudo → leer_y_limpiar() → agregar_mes() → 1 fila de métricas

El DataFrame intermedio (100k+ filas) se descarta después de agregar.
Solo persiste la serie temporal agregada (41 filas).
"""

import pandas as pd
from pathlib import Path

from config import (
    PATHS,
    CSV_ENCODING,
    DTYPE_TRANSFERENCIAS,
    COLUMNAS_TRANSFERENCIAS,
    TRAMITES_EXCLUIDOS_USADOS,
    TRAMITES_EXCLUIDOS_0KM,
    ANIO_MODELO_MIN,
    ORIGEN_PROTOCOLO21,
)


# ---------------------------------------------------------------------------
# FUNCIÓN 1 — Lectura y limpieza
# ---------------------------------------------------------------------------

def leer_y_limpiar(csv_path: Path, anio: int, tramites_excluidos: list) -> pd.DataFrame:
    """
    Lee un CSV mensual de transferencias DNRPA y aplica limpieza estándar.

    Parámetros
    ----------
    csv_path : Path
        Ruta al archivo CSV crudo.
    anio : int
        Año del archivo — define el límite superior de año modelo válido.
    tramites_excluidos : list
        Lista de strings a excluir por str.contains().
        Distinta para 'usados' y '0km' — ver config.py.

    Retorna
    -------
    pd.DataFrame
        DataFrame limpio con columna 'antiguedad' construida.
        Sin filas con año modelo nulo, fuera de rango o tramite excluido.
    """
    df = pd.read_csv(
        csv_path,
        encoding=CSV_ENCODING,
        sep=",",
        low_memory=False,
        usecols=COLUMNAS_TRANSFERENCIAS,
        dtype=DTYPE_TRANSFERENCIAS,
    )

    registros_originales = len(df)

    # Filtro 1 — excluir trámites no comerciales
    # Usa el parámetro tramites_excluidos, no una constante global
    mask_excluidos = df["tramite_tipo"].str.upper().str.contains(
        "|".join(tramites_excluidos), na=False
    )
    df = df[~mask_excluidos].copy()

    # Filtro 2 — excluir nulos en año modelo
    df = df.dropna(subset=["automotor_anio_modelo"])

    # Filtro 3 — excluir años fuera de rango válido
    df["automotor_anio_modelo"] = pd.to_numeric(
        df["automotor_anio_modelo"], errors="coerce"
    ).astype("Int64")

    df = df[
        (df["automotor_anio_modelo"] >= ANIO_MODELO_MIN) &
        (df["automotor_anio_modelo"] <= anio)
    ].copy()

    # Variable derivada — antigüedad en años
    df["antiguedad"] = anio - df["automotor_anio_modelo"]

    registros_finales = len(df)
    pct_retenidos = registros_finales / registros_originales * 100

    print(
        f"  {registros_originales:>8,} originales → "
        f"{registros_finales:>8,} limpios "
        f"({pct_retenidos:.1f}%)"
    )

    return df


# ---------------------------------------------------------------------------
# FUNCIÓN 2 — Agregación mensual
# ---------------------------------------------------------------------------

def agregar_mes(df: pd.DataFrame, anio: int, mes: int) -> pd.DataFrame:
    """
    Calcula las métricas mensuales base para el ISA.

    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame limpio devuelto por leer_y_limpiar().
    anio, mes : int
        Identificadores temporales del archivo.

    Retorna
    -------
    pd.DataFrame
        Una fila con las métricas del mes.
    """
    total = len(df)

    antiguedad_media = df["antiguedad"].mean()

    pct_protocolo21 = (
        (df["automotor_origen"] == ORIGEN_PROTOCOLO21).sum() / total * 100
    )

    pct_jovenes = (
        (df["antiguedad"] <= 3).sum() / total * 100
    )

    return pd.DataFrame([{
        "periodo":          f"{anio}-{mes:02d}",
        "anio":             anio,
        "mes":              mes,
        "total":            total,
        "antiguedad_media": round(antiguedad_media, 4),
        "pct_protocolo21":  round(pct_protocolo21, 4),
        "pct_jovenes":      round(pct_jovenes, 4),
    }])


# ---------------------------------------------------------------------------
# FUNCIÓN 3 — Orquestador
# ---------------------------------------------------------------------------

def construir_serie(tipo: str = "usados") -> pd.DataFrame:
    """
    Procesa todos los CSVs disponibles y construye la serie temporal.

    Parámetros
    ----------
    tipo : str
        'usados' → Raw_Usados / transferencias
        '0km'    → Raw_0km / inscripciones iniciales

    Retorna
    -------
    pd.DataFrame
        Serie temporal completa, ordenada cronológicamente.
        Una fila por mes disponible.
    """
    if tipo == "usados":
        raw_dir            = PATHS["raw_usados"]
        prefix             = "dnrpa-transferencias-autos-"
        tramites_excluidos = TRAMITES_EXCLUIDOS_USADOS
    elif tipo == "0km":
        raw_dir            = PATHS["raw_0km"]
        prefix             = "dnrpa-inscripciones-iniciales-autos-"
        tramites_excluidos = TRAMITES_EXCLUIDOS_0KM
    else:
        raise ValueError(f"tipo debe ser 'usados' o '0km', recibido: '{tipo}'")

    archivos = sorted(raw_dir.glob(f"{prefix}*.csv"))

    if not archivos:
        raise FileNotFoundError(
            f"No se encontraron archivos en {raw_dir} con prefijo '{prefix}'"
        )

    print(f"CONSTRUYENDO SERIE — {tipo.upper()}")
    print(f"Archivos encontrados: {len(archivos)}")
    print("=" * 60)

    filas = []

    for csv_path in archivos:
        stem         = csv_path.stem
        codigo_fecha = stem.replace(prefix, "")
        anio         = int(codigo_fecha[:4])
        mes          = int(codigo_fecha[4:6])

        print(f"{anio}-{mes:02d}", end=" → ")

        df_mes = leer_y_limpiar(csv_path, anio, tramites_excluidos)
        fila   = agregar_mes(df_mes, anio, mes)
        filas.append(fila)

        del df_mes

    serie = pd.concat(filas, ignore_index=True)
    serie = serie.sort_values(["anio", "mes"]).reset_index(drop=True)

    print("=" * 60)
    print(f"Serie construida: {len(serie)} meses")
    print(f"Período: {serie['periodo'].iloc[0]} → {serie['periodo'].iloc[-1]}")

    return serie