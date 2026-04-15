from nuvas_integrador.data.loader import load_csv
from nuvas_integrador.data.simulator import export_dataset, generate_synthetic_dataset, validar_hu3
from nuvas_integrador.processing.cleaning import limpiar_datos
from nuvas_integrador.processing.explorer import reporte_exploratorio
from nuvas_integrador.config import DATA_PROCESSED, DATA_RAW


def _imprimir_bloque(titulo: str) -> None:
    print()
    print(f"{titulo}")


def _imprimir_reporte_limpieza(reporte: dict) -> None:
    filas_antes = reporte["filas_antes"]
    filas_despues = reporte["filas_despues"]
    duplicados_eliminados = reporte["duplicados_eliminados"]
    nulos_antes = reporte["nulos_por_columna_antes"]
    nulos_despues = reporte["nulos_por_columna_despues"]
    mapeo_tipos = reporte["mapeo_tipos_aplicado"]
    transformaciones = reporte["transformaciones"]

    _imprimir_bloque("HU1 Limpieza de datos")
    print("Resumen")
    print(f"Filas antes: {filas_antes}")
    print(f"Filas despues: {filas_despues}")
    print(f"Duplicados eliminados: {duplicados_eliminados}")

    _imprimir_bloque("Nulos por columna antes")
    for columna, valor in nulos_antes.items():
        print(f"{columna}: {valor}")

    _imprimir_bloque("Nulos por columna despues")
    for columna, valor in nulos_despues.items():
        print(f"{columna}: {valor}")

    _imprimir_bloque("Mapeo de tipos aplicado")
    if mapeo_tipos:
        for columna, tipo_objetivo in mapeo_tipos.items():
            print(f"{columna}: {tipo_objetivo}")
    else:
        print("No se aplico mapeo de tipos")

    _imprimir_bloque("Transformaciones ejecutadas")
    for indice, paso in enumerate(transformaciones, start=1):
        print(f"{indice}. {paso}")


def _imprimir_reporte_exploracion(df_limpio, exploracion: dict) -> None:
    _imprimir_bloque("HU2 Exploracion con Pandas")
    print("Muestra inicial")
    print(df_limpio.head())

    _imprimir_bloque("Muestra final")
    print(df_limpio.tail())

    tipos_por_columna = {columna: str(tipo) for columna, tipo in df_limpio.dtypes.items()}

    _imprimir_bloque("Estructura")
    print(f"Filas: {exploracion['shape']['rows']}")
    print(f"Columnas: {exploracion['shape']['columns']}")
    print("Tipos por columna")
    print(tipos_por_columna)

    _imprimir_bloque("Describe numerico")
    print(df_limpio.describe(include=["number"]))

    _imprimir_bloque("Resumen extra")
    print(f"Total de columnas: {len(exploracion['column_names'])}")
    print(f"Columnas numericas: {len(exploracion['numeric_columns'])}")
    print(f"Columnas categoricas: {len(exploracion['categorical_columns'])}")


def _simular_y_exportar() -> None:
    _imprimir_bloque("HU3 Simulacion y exportacion")
    df_sintetico = generate_synthetic_dataset(num_records=1000)
    ruta_csv = DATA_PROCESSED / "synthetic_data.csv"
    ruta_json = DATA_PROCESSED / "synthetic_data.json"

    export_dataset(df_sintetico, ruta_csv, ruta_json)

    print(f"Dataset sintetico generado: {df_sintetico.shape[0]} filas")
    print(f"Cantidad de columnas: {df_sintetico.shape[1]}")
    print(f"CSV exportado en: {ruta_csv}")
    print(f"JSON exportado en: {ruta_json}")

    resultados_hu3 = validar_hu3(df_sintetico, ruta_csv, ruta_json)
    _imprimir_bloque("Validacion HU3")
    for criterio, cumple in resultados_hu3.items():
        estado = "OK" if cumple else "ERROR"
        print(f"{estado} - {criterio}")


def main():
    _simular_y_exportar()

    path = DATA_RAW / "data.csv"
    if not path.exists():
        raise FileNotFoundError(
            f"No se encontro el archivo: {path}. Crea data/raw/data.csv para ejecutar el flujo."
        )

    df = load_csv(path)

    _imprimir_bloque("Carga de dataset")
    print("Dataset cargado correctamente")
    print(f"Filas: {df.shape[0]} | Columnas: {df.shape[1]}")

    resultado_limpieza = limpiar_datos(
        df,
        mapeo_tipos={
            "fecha": "datetime",
            "monto": "float",
        },
    )

    exploracion = reporte_exploratorio(resultado_limpieza.cleaned_df)

    _imprimir_reporte_limpieza(resultado_limpieza.report)
    _imprimir_reporte_exploracion(resultado_limpieza.cleaned_df, exploracion)

if __name__ == "__main__":
    main()
