from __future__ import annotations

from io import StringIO
from typing import Any

import pandas as pd


def basic_stats(df: pd.DataFrame) -> dict[str, Any]:
    """Return compact quality and size metrics."""

    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": df.columns.tolist(),
        "nulls_by_column": df.isna().sum().to_dict(),
    }


def exploratory_report(df: pd.DataFrame) -> dict[str, Any]:
    """Build a full exploratory description using core Pandas operations."""

    info_buffer = StringIO()
    df.info(buf=info_buffer)

    numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_columns = df.select_dtypes(include=["object", "string", "category"]).columns.tolist()

    return {
        "head": df.head().to_dict(orient="records"),
        "tail": df.tail().to_dict(orient="records"),
        "info": info_buffer.getvalue(),
        "describe_numeric": df.describe(include=["number"]).to_dict(),
        "shape": {"rows": df.shape[0], "columns": df.shape[1]},
        "column_names": df.columns.tolist(),
        "numeric_columns": numeric_columns,
        "categorical_columns": categorical_columns,
    }


def group_by_example(df: pd.DataFrame, column: str) -> pd.Series:
    return df.groupby(column).size()
