import pandas as pd
from pathlib import Path

# --- Cargar serie usados ---
ruta = Path(r"C:\Users\usuario\Documents\PORTFOLIO\mercado-limones-causal\data\processed\serie_usados.parquet")
serie = pd.read_parquet(ruta)

# --- Filtrar período base: 2023 ---
base = serie[serie["anio"] == 2023].copy()

# --- Diagnóstico 1: valores del período base ---
print("=== PERÍODO BASE 2023 ===")
print(base[["periodo", "antiguedad_media", "pct_protocolo21"]].to_string(index=False))

# --- Diagnóstico 2: correlación entre componentes ---
print("\n=== CORRELACIÓN (Pearson) ===")
corr = base[["antiguedad_media", "pct_protocolo21"]].corr()
print(corr.round(4))

# --- Diagnóstico 3: parámetros del período base ---
print("\n=== PARÁMETROS DE NORMALIZACIÓN (a guardar en config.py) ===")
for col in ["antiguedad_media", "pct_protocolo21"]:
    media = base[col].mean()
    desvio = base[col].std(ddof=1)
    print(f"{col}:")
    print(f"  media  = {media:.4f}")
    print(f"  desvio = {desvio:.4f}")
# ---
# Lo que revelan los datos
# La correlación de -0.8916 es muy fuerte y negativa. 
# Traducido: en condiciones normales de mercado (2023), cuando la antigüedad sube, el Protocolo 21 baja, y viceversa. 
# Se mueven casi como imagen especular.
#
# #l patrón en los propios datos:
# 2023-07: antiguedad = 14.07 (mínimo)  →  protocolo21 = 40.75 (alto)
# 2023-11: antiguedad = 14.75 (máximo)  →  protocolo21 = 38.42 (mínimo)
# Hay una explicación económica directa: 
# Los vehículos Protocolo 21 son importaciones recientes del Mercosur, por lo tanto son más jóvenes en promedio.
# Cuando su participación sube, bajan la antigüedad media del mercado. Son dos caras del mismo fenómeno.
#
# El problema para el ISA
# Si se aplica la fórmula original tal cual:
# ISA = z(antiguedad_media) * 0.5 + z(pct_protocolo21) * 0.5
# Cuando el mercado se deteriora y la antigüedad sube, el protocolo21 baja — sus z-scores van en direcciones opuestas y se cancelan parcialmente.
# El índice amortigua la señal real en lugar de amplificarla.

# ---
