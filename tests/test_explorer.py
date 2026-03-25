import pandas as pd
from nuvas_integrador.processing.explorer import basic_stats, exploratory_report


def test_basic_stats():
    df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    stats = basic_stats(df)
    assert stats["rows"] == 3
    assert stats["columns"] == 2
    assert stats["column_names"] == ["a", "b"]


def test_exploratory_report_covers_hu2_acceptance_criteria():
    df = pd.DataFrame(
        {
            "edad": [22, 31, 27, 45, 38, 29],
            "ingreso": [1500.0, 2300.5, 1700.0, 4200.0, 3100.2, 2600.0],
            "segmento": ["a", "b", "a", "c", "b", "a"],
        }
    )

    report = exploratory_report(df)

    assert len(report["head"]) == 5
    assert len(report["tail"]) == 5
    assert "Data columns" in report["info"]
    assert "edad" in report["describe_numeric"]
    assert report["shape"] == {"rows": 6, "columns": 3}
    assert report["column_names"] == ["edad", "ingreso", "segmento"]
    assert report["numeric_columns"] == ["edad", "ingreso"]
    assert report["categorical_columns"] == ["segmento"]
