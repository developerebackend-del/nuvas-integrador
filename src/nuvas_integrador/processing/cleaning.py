from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd


@dataclass(frozen=True)
class ResultadoLimpieza:
    """Contenedor del resultado del proceso de limpieza del dataset."""

    cleaned_df: pd.DataFrame
    report: dict[str, Any]


def _normalizar_nombres_columnas(df: pd.DataFrame) -> pd.DataFrame:
    df_normalizado = df.copy()
    df_normalizado.columns = [str(col).strip().lower().replace(" ", "_") for col in df_normalizado.columns]
    return df_normalizado


def _normalizar_texto_columnas(df: pd.DataFrame) -> pd.DataFrame:
    df_normalizado = df.copy()
    columnas_texto = df_normalizado.select_dtypes(include=["object", "string"]).columns
    for col in columnas_texto:
        df_normalizado[col] = (
            df_normalizado[col]
            .astype("string")
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
            .str.lower()
        )
    return df_normalizado


def _corregir_tipos(df: pd.DataFrame, mapeo_tipos: dict[str, str] | None) -> pd.DataFrame:
    if not mapeo_tipos:
        return df

    df_tipos = df.copy()
    for columna, tipo_objetivo in mapeo_tipos.items():
        if columna not in df_tipos.columns:
            continue

        if tipo_objetivo == "datetime":
            df_tipos[columna] = pd.to_datetime(df_tipos[columna], errors="coerce")
        elif tipo_objetivo in {"int", "integer", "float", "number"}:
            df_tipos[columna] = pd.to_numeric(df_tipos[columna], errors="coerce")
            if tipo_objetivo in {"int", "integer"}:
                df_tipos[columna] = df_tipos[columna].astype("Int64")
        elif tipo_objetivo in {"str", "string", "text"}:
            df_tipos[columna] = df_tipos[columna].astype("string")

    return df_tipos


def limpiar_datos(
    df: pd.DataFrame,
    *,
    mapeo_tipos: dict[str, str] | None = None,
    eliminar_filas_con_nulos: bool = True,
    normalizar_texto: bool = True,
) -> ResultadoLimpieza:
    """Limpia un dataset y retorna los datos limpios junto con su reporte."""

    df_trabajo = _normalizar_nombres_columnas(df)
    transformaciones: list[str] = ["Columnas normalizadas (trim/lower/snake_case)."]

    nulos_antes = df_trabajo.isna().sum().to_dict()

    filas_antes = len(df_trabajo)
    df_trabajo = df_trabajo.drop_duplicates()
    duplicados_eliminados = filas_antes - len(df_trabajo)
    transformaciones.append(f"Filas duplicadas eliminadas: {duplicados_eliminados}.")

    if normalizar_texto:
        df_trabajo = _normalizar_texto_columnas(df_trabajo)
        transformaciones.append("Texto normalizado (trim, espacios internos y minusculas).")

    if mapeo_tipos:
        df_trabajo = _corregir_tipos(df_trabajo, mapeo_tipos)
        transformaciones.append("Coercion de tipos aplicada segun mapeo_tipos.")

    if eliminar_filas_con_nulos:
        filas_antes_dropna = len(df_trabajo)
        df_trabajo = df_trabajo.dropna().reset_index(drop=True)
        filas_nulos_eliminadas = filas_antes_dropna - len(df_trabajo)
        transformaciones.append(f"Filas con nulos eliminadas: {filas_nulos_eliminadas}.")

    nulos_despues = df_trabajo.isna().sum().to_dict()

    reporte: dict[str, Any] = {
        "filas_antes": len(df),
        "filas_despues": len(df_trabajo),
        "nulos_por_columna_antes": nulos_antes,
        "nulos_por_columna_despues": nulos_despues,
        "duplicados_eliminados": duplicados_eliminados,
        "mapeo_tipos_aplicado": mapeo_tipos or {},
        "transformaciones": transformaciones,
    }

    return ResultadoLimpieza(cleaned_df=df_trabajo, report=reporte)
