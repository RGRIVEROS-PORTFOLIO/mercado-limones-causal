import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

import pandas as pd
from metricas import calcular_isa
from config import PATHS

serie = pd.read_parquet(PATHS["processed"] / "serie_usados.parquet")
serie_isa = calcular_isa(serie)

print("=== ISA — SERIE COMPLETA ===")
cols = ["periodo", "antiguedad_media", "pct_protocolo21",
        "z_antiguedad", "z_protocolo21", "ISA"]
print(serie_isa[cols].to_string(index=False))

print("\n=== VERIFICACIÓN PERÍODO BASE 2023 ===")
base = serie_isa[serie_isa["anio"] == 2023]
print(f"ISA medio 2023:  {base['ISA'].mean():.4f}  (esperado ≈ 0.00)")
print(f"ISA desvío 2023: {base['ISA'].std():.4f}  (esperado ≈ 0.70)")

print("\n=== PICOS Y VALLES ===")
print(f"ISA máximo: {serie_isa.loc[serie_isa['ISA'].idxmax(), 'periodo']}"
      f"  →  {serie_isa['ISA'].max():.4f}")
print(f"ISA mínimo: {serie_isa.loc[serie_isa['ISA'].idxmin(), 'periodo']}"
      f"  →  {serie_isa['ISA'].min():.4f}")
print(f"\nRégimen usado: {serie_isa['regimen_id'].iloc[0]}")
print(f"Columnas del output: {list(serie_isa.columns)}")

output_path = PATHS["processed"] / "serie_isa.parquet"
serie_isa.to_parquet(output_path, index=False)
print(f"Guardado en: {output_path}")
print(f"Shape: {serie_isa.shape}")