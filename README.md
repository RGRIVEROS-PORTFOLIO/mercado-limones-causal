[Banner](reports/figures/Banner.png)

# Mercado de Limones Argentino — Inferencia Causal

> **¿El mercado de autos 0km deteriora la calidad del mercado de usados?**
> Análisis de series temporales (41 meses) para testear el efecto cascada
> descripto por Akerlof (1970) en el mercado automotor argentino.

---

## El problema

En el mercado automotor argentino, los compradores de autos usados enfrentan
**asimetría de información**: el vendedor sabe si el auto es un "limón" (baja
calidad), el comprador no. Akerlof (1970) demostró que esta asimetría expulsa
progresivamente a los compradores solventes del mercado secundario, degradando
su calidad promedio.

**La hipótesis de este proyecto:** cuando el mercado de 0km sufre un shock
(sobrestock, devaluación, apertura de importaciones), los compradores solventes
migran al mercado primario, dejando el mercado de usados con mayor proporción
de "limones". Este efecto cascada tarda entre 1 y 4 meses en transmitirse.

---

## Hallazgos principales

| Test | Resultado | Interpretación |
|---|---|---|
| Engle-Granger | p=0.0025 ✅ | Cointegración confirmada — relación estructural de largo plazo |
| Granger (lags 1-4) | p<0.05 ✅ | El 0km precede temporalmente al ISA |
| CCF lag óptimo | r=-0.452, lag=2 | El efecto cascada tarda ~60 días en transmitirse |
| ADL ISA(t-1) | coef=0.72, p<0.001 | El mercado de usados tiene memoria fuerte |
| Sensibilidad ISA | Parcial ⚠️ | Resultado sensible a la ponderación del índice |

**Decisión Metodológica C — Evidencia Parcial:**
Se detecta precedencia temporal del 0km sobre el ISA, consistente con la
hipótesis del efecto cascada, pero sensible a la especificación del índice
y potencialmente contaminada por variables macroeconómicas omitidas
(tipo de cambio, IPC, Badlar).

---

## Estructura del proyecto

```
mercado-limones-causal/
├── data/
│   ├── Raw_0km/              # CSVs crudos DNRPA — no versionados (1.4 GB+)
│   ├── Raw_Usados/           # CSVs crudos DNRPA — no versionados (1.4 GB+)
│   └── processed/
│       ├── serie_usados.parquet   # Serie mensual usados (41 meses)
│       ├── serie_0km.parquet      # Serie mensual 0km (41 meses)
│       └── serie_isa.parquet      # ISA calculado (output de metricas.py)
├── notebooks/
│   ├── 01_Ingesta_transferencias.ipynb   # ETL mercado de usados
│   ├── 02_Ingesta_0km.ipynb              # ETL mercado 0km
│   ├── 03_Analisis_causal.ipynb          # Análisis principal ← empezar aquí
│   └── exploratorio/                     # Scripts de diagnóstico metodológico
├── src/
│   ├── config.py             # Paths, parámetros, constantes
│   ├── pipeline.py           # ETL modular
│   ├── metricas.py           # Cálculo del ISA (arquitectura multi-régimen)
│   └── visualizacion.py      # Módulo de graficado desacoplado
├── reports/
│   └── figures/              # Visualizaciones generadas
│   |   ├── 01_series_temporales.png
│   |   ├── 02_ccf.png
│   |   ├── 03_sensibilidad_isa.png
│   |   └── 04_residuos_adl.png
|   |___doc/
|       |__informe_bancos
|       |__informe_concesionarios
|       |__informe_publico 
├── environment.yml           # Dependencias Conda
└── README.md
```

---

## Reproducibilidad

### Requisitos

- Python 3.10+ (Conda recomendado)
- Datos crudos de la DNRPA en `data/Raw_0km/` y `data/Raw_Usados/`

### Instalación

```bash
git clone https://github.com/RGRIVEROS-PORTFOLIO/mercado-limones-causal
cd mercado-limones-causal
conda env create -f environment.yml
conda activate limones-causal
```

### Ejecución

```bash
# Opción A — reproducir desde cero
jupyter notebook notebooks/01_Ingesta_transferencias.ipynb
jupyter notebook notebooks/02_Ingesta_0km.ipynb
jupyter notebook notebooks/03_Analisis_causal.ipynb

# Opción B — análisis causal directo (series ya procesadas disponibles)
jupyter notebook notebooks/03_Analisis_causal.ipynb
```

---

## Decisiones metodológicas documentadas

### Índice de Selección Adversa (ISA)

El ISA es un z-score compuesto de dos variables de la DNRPA:

```
ISA = z(antiguedad_media) * 0.5 + (-z(pct_protocolo21)) * 0.5
```

**Decisiones clave:**

| Decisión | Justificación |
|---|---|
| Período base: 2023 | Año pre-shock Milei — comportamiento estructural sin perturbaciones |
| Parámetros fijos | Permite incorporar datos futuros sin recalibrar la escala histórica |
| Signo negativo en pct_protocolo21 | Correlación Pearson = -0.89 con antigüedad en período base. Mayor participación Protocolo 21 rejuvenece el parque, reduciendo deterioro |
| Ponderación 50/50 | Base. Validada por análisis de sensibilidad 70/30 y 30/70 |

### Arquitectura multi-régimen

El ISA es sensible a rupturas estructurales. El módulo `metricas.py` implementa
una arquitectura extensible: ante un nuevo régimen (político, cambiario, regulatorio),
se agrega un ítem a `REGIMENES` sin modificar los parámetros históricos.

```python
# Agregar nuevo régimen en 2027 — sin tocar la serie histórica
REGIMENES = [
    {"id": "2023_base", ...},  # ← nunca se modifica
    {"id": "2027_base", ...},  # ← se agrega aquí
]
```

---

## Limitaciones

**Estructurales (heredadas de los datos DNRPA):**
- **Punto ciego de Akerlof:** se registran transacciones completadas, no intentos fallidos
- **Ausencia de precios:** el análisis es volumétrico y composicional, sin cuantificación en pesos
- **Subregistro estacional:** diciembre presenta anomalías sistemáticas por liquidación de stock

**Metodológicas:**
- **Endogeneidad:** tipo de cambio, IPC y Badlar afectan simultáneamente a ambos mercados
  y no fueron incluidos como controles. Los coeficientes del 0km pueden estar contaminados
- **Ruptura estructural 2024:** la desregulación de importaciones (Decreto 49/2025,
  Resolución 271/2025) cambió la naturaleza de `pct_protocolo21` en el mercado de usados
- **Sensibilidad del ISA:** el resultado de Granger es significativo con ponderación 50/50
  (p=0.041) pero marginal con 70/30 (p=0.052) y no significativo con 30/70 (p=0.104)

---

## Protocolo de actualización (2027+)

### Paso 1 — Evaluar el contexto

Antes de correr cualquier código, responder:

- ¿Hubo una ruptura estructural desde el último análisis?
  - Cambio de política cambiaria significativo
  - Apertura o cierre de importaciones automotrices
  - Crisis sistémica (cepo, default, híper)

**Si no hubo ruptura → Paso 2A**
**Si hubo ruptura → Paso 2B**

### Paso 2A — Actualización sin ruptura

```bash
# 1. Descargar nuevos CSVs de la DNRPA a data/Raw_*/
# 2. Reconstruir series
jupyter notebook notebooks/01_Ingesta_transferencias.ipynb
jupyter notebook notebooks/02_Ingesta_0km.ipynb
# 3. El ISA se recalcula automáticamente con parámetros 2023_base
jupyter notebook notebooks/03_Analisis_causal.ipynb
```

### Paso 2B — Recalibración por ruptura de régimen

```python
# En src/metricas.py — agregar nuevo régimen
REGIMENES = [
    {"id": "2023_base", ...},   # NO MODIFICAR
    {
        "id":            "2027_base",
        "label":         "Descripción del nuevo régimen",
        "vigente_desde": "2027-01",
        "vigente_hasta": "2027-12",
        "params": {
            "antiguedad_media": {"media": X.XXXX, "desvio": X.XXXX},
            "pct_protocolo21":  {"media": XX.XXXX, "desvio": X.XXXX},
        },
    },
]

# Calcular parámetros del nuevo período base
base_nueva = serie[serie["anio"] == 2027]
print(base_nueva[["antiguedad_media", "pct_protocolo21"]].describe())
```

---

## Extensiones recomendadas

| Prioridad | Extensión | Impacto esperado |
|---|---|---|
| Alta | Controles macro (IPC, tipo de cambio, Badlar) | Resolver endogeneidad — confirmar efecto cascada puro |
| Alta | Dummy estacional diciembre | Limpiar anomalía sistemática de fin de año |
| Media | Modelo de Corrección de Errores (ECM) | Cuantificar velocidad de ajuste al equilibrio de largo plazo |
| Media | Recalibrar ISA con período base post-2024 | Mejorar poder interpretativo en régimen de apertura |
| Baja | Dashboard interactivo (Looker Studio / Power BI) | Democratizar el termómetro para equipos no técnicos |

---

## Proyecto antecedente

Este proyecto es la continuación directa de:

**[Mercado de Limones Argentino — Análisis Descriptivo](https://github.com/RGRIVEROS-PORTFOLIO/mercado-limones-argentina)**

El antecedente construyó las "instantáneas" del mercado (análisis cross-seccional).
Este proyecto construye la **serie temporal continua** y aplica inferencia causal
para testear el mecanismo de transmisión entre mercados.

---

## Fuente de datos

**DNRPA** — Dirección Nacional de los Registros de la Propiedad Automotor
Portal de datos abiertos: [datos.gob.ar](https://datos.gob.ar)
Período: Enero 2023 — Mayo 2026

---

## Autor

**Rodolfo Gabriel Riveros Lobos**
Analista de Datos — San Juan, Argentina
[[Linkedin/RGRIVEROS](https://www.linkedin.com/in/rgriveros/)]
Mail: rgriveros@gmail.com
[![GitHub](https://img.shields.io/badge/GitHub-RGRIVEROS--PORTFOLIO-black)](https://github.com/RGRIVEROS-PORTFOLIO)

---

*Proyecto desarrollado con Python, statsmodels, pandas y buenas prácticas
de computación científica (Wilson et al., 2017).*
