from nuvas_integrador.data.loader import load_csv
from nuvas_integrador.processing.cleaning import clean_data
from nuvas_integrador.processing.explorer import exploratory_report
from nuvas_integrador.config import DATA_RAW


def _print_cleaning_report(report: dict) -> None:
    print("\n--- HU1 Limpieza de Datos ---")
    print("Resumen general:")
    print(f"- Filas antes: {report['rows_before']}")
    print(f"- Filas despues: {report['rows_after']}")
    print(f"- Duplicados eliminados: {report['duplicates_removed']}")

    print("\nNulos por columna (antes):")
    for column, value in report["nulls_by_column_before"].items():
        print(f"- {column}: {value}")

    print("\nNulos por columna (despues):")
    for column, value in report["nulls_by_column_after"].items():
        print(f"- {column}: {value}")

    print("\nMapeo de tipos aplicado:")
    if report["applied_type_mapping"]:
        for column, target_type in report["applied_type_mapping"].items():
            print(f"- {column}: {target_type}")
    else:
        print("- No se aplico mapeo de tipos")

    print("\nTransformaciones ejecutadas:")
    for index, step in enumerate(report["transformations"], start=1):
        print(f"{index}. {step}")


def main():
    path = DATA_RAW / "data.csv"
    if not path.exists():
        raise FileNotFoundError(
            f"No se encontro el archivo: {path}. Crea data/raw/data.csv para ejecutar el flujo."
        )

    df = load_csv(path)

    print("Dataset cargado correctamente")
    print(f"Filas: {df.shape[0]} | Columnas: {df.shape[1]}")

    cleaning_result = clean_data(
        df,
        type_mapping={
            "fecha": "datetime",
            "monto": "float",
        },
    )

    exploration = exploratory_report(cleaning_result.cleaned_df)

    _print_cleaning_report(cleaning_result.report)

    print("\n--- HU2 Exploracion con Pandas ---")
    print("head():")
    print(cleaning_result.cleaned_df.head())
    print("\ntail():")
    print(cleaning_result.cleaned_df.tail())

    column_types = {
        column: str(dtype)
        for column, dtype in cleaning_result.cleaned_df.dtypes.items()
    }

    print("\nEstructura (resumen):")
    print(f"Filas: {exploration['shape']['rows']} | Columnas: {exploration['shape']['columns']}")
    print("Tipos por columna:")
    print(column_types)

    print("describe() columnas numericas:")
    print(cleaning_result.cleaned_df.describe(include=["number"]))
    print("\nResumen de estructura:")
    print(exploration["shape"])
    print("Nombres de columnas:")
    print(exploration["column_names"])
    print("Columnas numericas:")
    print(exploration["numeric_columns"])
    print("Columnas categoricas:")
    print(exploration["categorical_columns"])

if __name__ == "__main__":
    main()
