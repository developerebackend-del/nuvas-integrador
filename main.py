from io import StringIO
from pathlib import Path

import pandas as pd

from notebook.limpieza import documentar_transformaciones, limpiar_datos
from notebook.descripcion import describir_datos
from utils.simulacion import generar_simulacion


def describir_data_frame(df):
    """Retorna un resumen exploratorio para HU2 en JSON."""
    buffer = StringIO()
    df.info(buf=buffer)

    columnas_numericas = df.select_dtypes(include=["number"]).columns.tolist()
    columnas_categoricas = df.select_dtypes(include=["object", "string", "category"]).columns.tolist()

    descripcion_numerica = (
        df.describe(include=["number"]).to_dict() if columnas_numericas else {}
    )
    descripcion_categorica = (
        df.describe(include=["object", "string", "category"]).to_dict()
        if columnas_categoricas
        else {}
    )

    return {
        "filas": int(df.shape[0]),
        "columnas": int(df.shape[1]),
        "nombres_variables": df.columns.tolist(),
        "head": df.head().to_dict(orient="records"),
        "tail": df.tail().to_dict(orient="records"),
        "info": buffer.getvalue(),
        "columnas_numericas": columnas_numericas,
        "columnas_categoricas": columnas_categoricas,
        "describe_numerico": descripcion_numerica,
        "describe_categorico": descripcion_categorica,
    }


def exportar_y_validar(df, ruta_csv, ruta_json):
    """Exporta a CSV/JSON y valida recarga sin perdida estructural relevante."""
    df.to_csv(ruta_csv, index=False)
    df.to_json(ruta_json, orient="records", date_format="iso")

    df_csv = pd.read_csv(ruta_csv)
    df_json = pd.read_json(ruta_json)

    misma_estructura = list(df.columns) == list(df_csv.columns) == list(df_json.columns)

    return {
        "csv_filas": int(len(df_csv)),
        "json_filas": int(len(df_json)),
        "filas_original": int(len(df)),
        "misma_estructura_columnas": misma_estructura,
    }


def main():
    # ZONA PARA IMPORTAR SIMULACIONES
    # (ya hecho arriba con: from utils.simulacion import generar_simulacion)

    # ZONA PARA IMPORTAR LIMPIEZAS
    # (ya hecho arriba con: from notebook.limpieza import limpiar_datos)

    # ZONA PARA IMPORTAR DESCRIPCIONES
    # (ya hecho arriba con: from notebook.descripcion import describir_datos)

    salida = Path("salidas")
    salida.mkdir(parents=True, exist_ok=True)

    # CREANDO LAS SIMULACIONES
    simulaciones = generar_simulacion(1200)

    # ORDENANDO LAS SIMULACIONES
    simulaciones_df = pd.DataFrame(simulaciones)

    # HU2: DESCRIPCION EXPLORATORIA SOBRE DATOS ORIGINALES
    print("\n=== EXPLORACION DE DATOS ORIGINALES (HU2) ===\n")
    reporte_exploratorio = describir_data_frame(simulaciones_df)
    pd.Series(reporte_exploratorio).to_json(
        salida / "reporte_exploratorio.json", force_ascii=False, indent=2
    )

    # LIMPIANDO EL SET DE DATOS (HU1)
    print("\n=== LIMPIANDO EL SET DE DATOS (HU1) ===\n")
    simulaciones_limpias, reporte_limpieza = limpiar_datos(simulaciones_df)
    documentar_transformaciones(reporte_limpieza, salida / "reporte_limpieza.md")

    # DESCRIBIENDO LOS DATOS (HU2)
    print("\n=== DESCRIPCION DETALLADA DE DATOS LIMPIOS (HU2) ===\n")
    describir_datos(simulaciones_limpias)

    # HU3: EXPORTACION Y VALIDACION
    print("\n=== EXPORTANDO A CSV Y JSON (HU3) ===\n")
    validacion = exportar_y_validar(
        simulaciones_limpias,
        salida / "simulaciones_limpias.csv",
        salida / "simulaciones_limpias.json",
    )

    print("Resumen del proceso:")
    print(f"- Registros simulados: {len(simulaciones_df)}")
    print(f"- Registros limpios: {len(simulaciones_limpias)}")
    print(f"- Reporte exploratorio: {salida / 'reporte_exploratorio.json'}")
    print(f"- Reporte limpieza: {salida / 'reporte_limpieza.md'}")
    print("- Validacion de exportacion:")
    print(f"  * Filas en CSV: {validacion['csv_filas']}")
    print(f"  * Filas en JSON: {validacion['json_filas']}")
    print(f"  * Filas en dataset limpio: {validacion['filas_original']}")
    if validacion["misma_estructura_columnas"]:
        print("  * Estructura de columnas: OK")
    else:
        print("  * Estructura de columnas: revisar")


if __name__ == "__main__":
    main()
