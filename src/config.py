"""
config.py — Configuración central del proyecto mercado-limones-causal

Fuente de verdad única para rutas, constantes y esquema de datos.
Todos los módulos importan desde aquí; ningún valor se repite en otro archivo.
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# RUTAS
# ---------------------------------------------------------------------------

def find_project_root(marker: str = "README.md") -> Path:
    """Encuentra la raíz del proyecto subiendo desde el directorio actual."""
    current = Path.cwd()
    for parent in [current] + list(current.parents):
        if (parent / marker).exists():
            return parent
    raise FileNotFoundError(
        f"No se encontró la raíz del proyecto (buscando '{marker}')"
    )

ROOT = find_project_root()

PATHS = {
    "raw_usados":  ROOT / "data" / "Raw_Usados",
    "raw_0km":     ROOT / "data" / "Raw_0km",
    "cache":       ROOT / "data" / "cache",
    "processed":   ROOT / "data" / "processed",
    "figures":     ROOT / "reports" / "figures",
}

# ---------------------------------------------------------------------------
# PARÁMETROS DE LECTURA CSV
# ---------------------------------------------------------------------------

CSV_ENCODING = "utf-8-sig"   # UTF-8 con BOM — estándar DNRPA

# Dtypes explícitos para evitar inferencia errónea de pandas
# Validados en proyecto anterior (01_exploracion.ipynb — enero 2023)
DTYPE_TRANSFERENCIAS = {
    "tramite_tipo":                    "str",
    "tramite_fecha":                   "str",   # se parsea después como fecha
    "fecha_inscripcion_inicial":       "str",   # ídem
    "registro_seccional_provincia":    "str",
    "automotor_origen":                "str",
    "automotor_anio_modelo":           "float64",  # tiene NaN → no puede ser int
    "automotor_tipo_codigo":           "str",   # valores mixtos
    "automotor_tipo_descripcion":      "str",
    "automotor_marca_descripcion":     "str",
    "automotor_uso_descripcion":       "str",
    "titular_tipo_persona":            "str",
    "titular_domicilio_provincia":     "str",
    "titular_genero":                  "str",
    "titular_anio_nacimiento":         "float64",  # tiene NaN ocasional
    "titular_pais_nacimiento":         "str",
}

# Columnas que SÍ cargamos (las demás se descartan en la lectura)
# Decisión documentada: excluimos códigos redundantes, modelo y columnas
# sin valor para el ISA. Ver 01_exploracion.ipynb del proyecto anterior.
COLUMNAS_TRANSFERENCIAS = list(DTYPE_TRANSFERENCIAS.keys())

# Ídem para inscripciones iniciales (0km) — mismo schema, mismas decisiones
DTYPE_0KM = DTYPE_TRANSFERENCIAS.copy()
COLUMNAS_0KM = COLUMNAS_TRANSFERENCIAS.copy()

# ---------------------------------------------------------------------------
# PARÁMETROS DE LIMPIEZA
# ---------------------------------------------------------------------------

# Tipos de trámite a excluir — no responden a dinámica comercial estándar
# Fuente: análisis tramite_tipo en 01_exploracion.ipynb
TRAMITES_EXCLUIDOS = [
    "SUBASTADO",
    "CLASICO",
    "SUBASTADO IMPORTADO",
]

# Rango válido de año de modelo
# Límite inferior: 1950 (registro DNRPA desde esa época)
# Límite superior: se calcula dinámicamente en pipeline (año del archivo + 1)
ANIO_MODELO_MIN = 1950

# ---------------------------------------------------------------------------
# PARÁMETROS DEL ISA
# ---------------------------------------------------------------------------

# Ponderaciones del Índice de Selección Adversa
# Componente 1: antigüedad promedio (z-score)
# Componente 2: participación de Protocolo 21 (z-score)
# Validado con análisis de sensibilidad 70/30 vs 50/50 en proyecto anterior
ISA_PESO_ANTIGUEDAD   = 0.5
ISA_PESO_PROTOCOLO21  = 0.5

# Valores de automotor_origen
ORIGEN_PROTOCOLO21 = "Protocolo 21"
ORIGEN_NACIONAL    = "Nacional"
ORIGEN_IMPORTADO   = "Importado"

# ---------------------------------------------------------------------------
# RANGOS DE ANTIGÜEDAD (para segmentación)
# Validados en 01_exploracion.ipynb
# ---------------------------------------------------------------------------

RANGOS_ANTIGUEDAD = {
    "0-3 años":   (0, 3),
    "4-7 años":   (4, 7),
    "8-15 años":  (8, 15),
    "16-25 años": (16, 25),
    "26-35 años": (26, 35),
    "36+ años":   (36, 999),
}