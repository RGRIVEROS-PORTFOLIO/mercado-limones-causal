from pathlib import Path
import pandas as pd

def cargar_mes(anio, mes, tipo="usados"):
    """
    Carga un mes específico de transferencias o inscripciones.
    tipo: 'usados' o '0km'
    """
    parquet_path = Path(f"data/cache/{tipo}_{anio}_{mes:02d}.parquet")
    if parquet_path.exists():
        print("Leyendo desde cache:", parquet_path)
        return pd.read_parquet(parquet_path)
    else:
        raw_dir = "Raw_Usados" if tipo == "usados" else "Raw_0km"
        prefix = "dnrpa-transferencias-autos" if tipo == "usados" else "dnrpa-inscripciones-iniciales-autos"
        pattern = f"{prefix}-{anio}{mes:02d}.csv"

        files = list(Path(f"data/{raw_dir}").glob(pattern))
        if not files:
            raise FileNotFoundError(f"No se encontró archivo {pattern} en {raw_dir}")
        csv_path = files[0]

        print("Leyendo CSV original:", csv_path)
        df = pd.read_csv(csv_path)
        df.to_parquet(parquet_path)
        return df

def cargar_serie_completa(tipo="usados"):
    """
    Carga todos los meses disponibles de transferencias o inscripciones.
    """
    raw_dir = "Raw_Usados" if tipo == "usados" else "Raw_0km"
    prefix = "dnrpa-transferencias-autos" if tipo == "usados" else "dnrpa-inscripciones-iniciales-autos"

    dfs = []
    for csv_file in Path(f"data/{raw_dir}").glob(f"{prefix}-*.csv"):
        df = pd.read_csv(csv_file)
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

