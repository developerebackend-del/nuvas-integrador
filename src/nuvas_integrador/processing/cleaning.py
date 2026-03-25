from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd


@dataclass(frozen=True)
class CleaningResult:
    """Result container for dataset cleaning process."""

    cleaned_df: pd.DataFrame
    report: dict[str, Any]


def _normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    normalized = df.copy()
    normalized.columns = [str(col).strip().lower().replace(" ", "_") for col in normalized.columns]
    return normalized


def _normalize_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    normalized = df.copy()
    object_columns = normalized.select_dtypes(include=["object", "string"]).columns
    for col in object_columns:
        normalized[col] = (
            normalized[col]
            .astype("string")
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
            .str.lower()
        )
    return normalized


def _coerce_types(df: pd.DataFrame, type_mapping: dict[str, str] | None) -> pd.DataFrame:
    if not type_mapping:
        return df

    coerced = df.copy()
    for column, target_type in type_mapping.items():
        if column not in coerced.columns:
            continue

        if target_type == "datetime":
            coerced[column] = pd.to_datetime(coerced[column], errors="coerce")
        elif target_type in {"int", "integer", "float", "number"}:
            coerced[column] = pd.to_numeric(coerced[column], errors="coerce")
            if target_type in {"int", "integer"}:
                coerced[column] = coerced[column].astype("Int64")
        elif target_type in {"str", "string", "text"}:
            coerced[column] = coerced[column].astype("string")

    return coerced


def clean_data(
    df: pd.DataFrame,
    *,
    type_mapping: dict[str, str] | None = None,
    drop_rows_with_nulls: bool = True,
    normalize_text: bool = True,
) -> CleaningResult:
    """Clean a dataset and return both cleaned data and transformation report."""

    working_df = _normalize_column_names(df)
    transformations: list[str] = ["Normalized column names (trim/lower/snake_case)."]

    nulls_before = working_df.isna().sum().to_dict()

    rows_before = len(working_df)
    working_df = working_df.drop_duplicates()
    duplicates_removed = rows_before - len(working_df)
    transformations.append(f"Removed duplicated rows: {duplicates_removed}.")

    if normalize_text:
        working_df = _normalize_text_columns(working_df)
        transformations.append(
            "Normalized text columns (trim spaces, collapse internal whitespace, lowercase)."
        )

    if type_mapping:
        working_df = _coerce_types(working_df, type_mapping)
        transformations.append("Applied explicit type coercion based on type_mapping.")

    if drop_rows_with_nulls:
        rows_before_dropna = len(working_df)
        working_df = working_df.dropna().reset_index(drop=True)
        dropped_rows = rows_before_dropna - len(working_df)
        transformations.append(f"Dropped rows containing nulls: {dropped_rows}.")

    nulls_after = working_df.isna().sum().to_dict()

    report: dict[str, Any] = {
        "rows_before": len(df),
        "rows_after": len(working_df),
        "nulls_by_column_before": nulls_before,
        "nulls_by_column_after": nulls_after,
        "duplicates_removed": duplicates_removed,
        "applied_type_mapping": type_mapping or {},
        "transformations": transformations,
    }

    return CleaningResult(cleaned_df=working_df, report=report)
