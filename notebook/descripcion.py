import pandas as pd


def describir_datos(data_frame_limpio):
    """Toda rutina de analisis debe describir el dataset.
    
    Es importante:
    1. Conocer cuantos registros tengo
    2. Conocer cuantos atributos tengo
    3. Tener acceso a una lista con los nombres de los atributos
    4. Hacer conteos de algunas columnas de interes
    5. Conocer las estadisticas descriptivas de los campos numericos
       (Media-max-min-std-percentiles)
    6. Si tengo fechas es util conocer cual es la fecha mas antigua y la fecha mas nueva
    """
    print("*** DESCRIPCION DEL DATASET ***")
    print(f"Numero de filas del dataset: {data_frame_limpio.shape[0]}")
    print(f"Numero de columnas del dataset: {data_frame_limpio.shape[1]}")
    print(f"Lista de columnas disponibles: {list(data_frame_limpio.columns)}")
    print(f"Tipos de dato de cada atributo:\n{data_frame_limpio.dtypes}\n")

    # ESTADISTICAS (SOLO APLICA PARA DATOS NUMERICOS)
    print("*** ESTADISTICAS NUMERICAS ***")
    columnas_numericas = data_frame_limpio.select_dtypes(include=["number"]).columns.tolist()
    if columnas_numericas:
        print(f"{data_frame_limpio[columnas_numericas].describe()}\n")
    else:
        print("No hay columnas numericas disponibles.\n")

    # INFORMACION DE CONTEOS VALIOSOS
    print("*** CONTEOS POR CATEGORIA ***")
    if "servicio" in data_frame_limpio.columns:
        print(f"Conteo de servicios:\n{data_frame_limpio['servicio'].value_counts()}\n")

    if "canal" in data_frame_limpio.columns:
        print(f"Conteo de canales:\n{data_frame_limpio['canal'].value_counts()}\n")

    if "ciudad" in data_frame_limpio.columns:
        print(f"Conteo de ciudades:\n{data_frame_limpio['ciudad'].value_counts()}\n")

    if "sucursal" in data_frame_limpio.columns:
        print(f"Conteo de sucursales:\n{data_frame_limpio['sucursal'].value_counts()}\n")

    if "metodo_pago" in data_frame_limpio.columns:
        print(f"Conteo de metodos de pago:\n{data_frame_limpio['metodo_pago'].value_counts()}\n")

    # DESCRIBIENDO LAS FECHAS
    if "fecha" in data_frame_limpio.columns:
        print("*** DESCRIPCION DE FECHAS ***")
        print(f"Fecha mas antigua: {data_frame_limpio['fecha'].min()}")
        print(f"Fecha mas reciente: {data_frame_limpio['fecha'].max()}\n")
