from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def generate_synthetic_dataset(num_records: int = 1000, seed: int = 42) -> pd.DataFrame:
    """Genera un dataset sintetico para pruebas y escenarios de demo."""

    rng = np.random.default_rng(seed)

    segments = np.array(["a", "b", "c", "d"])
    clients = np.array([
        "ana",
        "luis",
        "marta",
        "carlos",
        "sofia",
        "diego",
        "laura",
        "jose",
    ])

    dates = pd.date_range(start="2025-01-01", periods=365, freq="D")

    df = pd.DataFrame(
        {
            "id": np.arange(1, num_records + 1),
            "fecha": rng.choice(dates, size=num_records),
            "cliente": rng.choice(clients, size=num_records),
            "segmento": rng.choice(segments, size=num_records),
            "monto": np.round(rng.uniform(50, 5000, size=num_records), 2),
            "activo": rng.choice([True, False], size=num_records, p=[0.8, 0.2]),
        }
    )

    return df


def export_dataset(df: pd.DataFrame, csv_path: Path, json_path: Path) -> None:
    """Exporta un dataset a CSV y JSON conservando la misma estructura de columnas."""

    csv_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(csv_path, index=False)
    df.to_json(json_path, orient="records", date_format="iso", indent=2)


def validar_hu3(df_origen: pd.DataFrame, csv_path: Path, json_path: Path) -> dict[str, bool]:
    """Valida criterios de HU3 despues de generar y exportar el dataset sintetico."""

    csv_df = pd.read_csv(csv_path)
    json_df = pd.read_json(json_path)

    columnas_origen = list(df_origen.columns)

    resultados = {
        "dataset_sintetico_generado": len(df_origen) >= 1000 and df_origen.shape[1] >= 2,
        "registros_minimos": len(df_origen) >= 1000,
        "columnas_varias": df_origen.shape[1] >= 5,
        "csv_exportado": csv_path.exists(),
        "json_exportado": json_path.exists(),
        "estructura_csv_igual": list(csv_df.columns) == columnas_origen,
        "estructura_json_igual": list(json_df.columns) == columnas_origen,
        "tamano_csv_igual": len(csv_df) == len(df_origen),
        "tamano_json_igual": len(json_df) == len(df_origen),
    }

    return resultados
