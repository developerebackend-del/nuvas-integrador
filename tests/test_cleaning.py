import pandas as pd
from nuvas_integrador.processing.cleaning import clean_data


def test_clean_data_covers_hu1_acceptance_criteria():
    df = pd.DataFrame(
        {
            " Fecha ": ["2026-01-01", "2026-01-01", "bad_date", None],
            "Monto": ["100", "100", " 220.5 ", "foo"],
            "Cliente": [" Ana  ", " Ana  ", "  LUIS", "Marta"],
        }
    )

    result = clean_data(
        df,
        type_mapping={
            "fecha": "datetime",
            "monto": "float",
            "cliente": "string",
        },
    )

    cleaned = result.cleaned_df
    report = result.report

    assert report["nulls_by_column_before"]["fecha"] == 1
    assert report["duplicates_removed"] == 1
    assert str(cleaned["fecha"].dtype).startswith("datetime64")
    assert str(cleaned["monto"].dtype).lower().startswith("float")
    assert cleaned["cliente"].str.contains(r"\s{2,}").sum() == 0
    assert cleaned["cliente"].str.lower().equals(cleaned["cliente"])
    assert len(report["transformations"]) >= 4
