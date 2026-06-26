# Mercado de Limones Argentino: Inferencia Causal (2023–2026)

## Descripción

Evolución del análisis exploratorio inicial hacia un producto de datos
profesional enfocado en inferencia causal. El objetivo es cuantificar
cómo el sobrestock en el mercado de 0km actúa como variable predictora
del deterioro de calidad (selección adversa) en el mercado de usados
en Argentina.

## Marco Teórico

- **Akerlof (1970):** Selección adversa — la incertidumbre retira los
  "duraznos" (autos buenos) del mercado.
- **Jensen & Meckling (1976):** Problema principal-agente — el efecto
  diciembre como anomalía estacional.
- **Inferencia Causal:** Tests de Causalidad de Granger y modelos ADL
  para identificar el lag temporal del impacto del 0km en el usado.

## Antecedente

Este proyecto extiende el análisis exploratorio previo (enero 2023 –
marzo 2026, 1.025.853 transferencias, 7 puntos temporales) hacia una
serie continua de 41 meses con capacidad de inferencia estadística.

## Estructura

```text
mercado-limones-causal/
├── data/
│   ├── Raw_Usados/     # CSVs originales DNRPA — transferencias
│   ├── Raw_0km/        # CSVs originales DNRPA — inscripciones iniciales
│   ├── cache/          # Parquets por mes (generados por pipeline)
│   └── processed/      # Series temporales agregadas (output ETL)
├── src/
│   ├── config.py       # Rutas, constantes, dtypes
│   ├── pipeline.py     # ETL: CSV → limpieza → agregación → Parquet
│   ├── metricas.py     # Cálculo del ISA y sus componentes
│   └── visualizacion.py
├── notebooks/
│   ├── 01_Ingesta_transferencias.ipynb
│   ├── 02_Ingesta_0km.ipynb
│   └── 03_Analisis_causal.ipynb
├── reports/
│   ├── doc/
│   └── figures/
├── environment.yml
├── requirements.txt
└── README.md
```

## Instalación

```bash
conda env create -f environment.yml
conda activate limones-causal
```

## Fuente de Datos

DNRPA — Dirección Nacional de los Registros de la Propiedad del Automotor  
Portal: https://datos.gob.ar  
Período: enero 2023 – mayo 2026  
Volumen: ~20 millones de registros, 82 archivos CSV

## Autor

**Rodolfo Gabriel Riveros Lobos**  
Data Analyst Junior | Calidad ISO 9001 · Inferencia de Mercados  
[LinkedIn](https://linkedin.com/in/rgriveros) · [Portfolio](https://github.com/RGRIVEROS-PORTFOLIO)

---
*Licencia MIT*