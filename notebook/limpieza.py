from pathlib import Path

import pandas as pd


SERVICIOS_VALIDOS = ["mercado general", "aseo hogar", "frutas verduras"]
CIUDADES_VALIDAS = ["bogota", "medellin", "cali", "barranquilla", "bucaramanga"]
CANALES_VALIDOS = ["web", "caja", "app", "domicilio"]
SUCURSALES_VALIDAS = ["norte", "centro", "sur", "occidente"]
METODOS_PAGO_VALIDOS = ["efectivo", "tarjeta", "transferencia", "billetera digital"]


def limpiar_datos(data_frame_sucio):
    """Limpia el DataFrame y retorna el DataFrame limpio junto con un reporte."""
    data_frame_limpio = data_frame_sucio.copy()

    reporte = {
        "registros_iniciales": int(len(data_frame_limpio)),
        "nulos_iniciales_por_columna": data_frame_limpio.isna().sum().to_dict(),
        "duplicados_iniciales": int(data_frame_limpio.duplicated().sum()),
    }

    # PROCESANDO LOS TEXTOS DEL DF SUCIO
    # 1. Limpiando los textos para eliminar espacios y mayusculas
    data_frame_limpio["servicio"] = (
        data_frame_limpio["servicio"].astype("string").str.strip().str.lower()
    )
    data_frame_limpio["codigo"] = data_frame_limpio["codigo"].astype("string").str.strip().str.lower()

    # 2. Limpiando los textos para controlar valores inesperados
    valores_esperados_servicio = SERVICIOS_VALIDOS
    data_frame_limpio["servicio"] = data_frame_limpio["servicio"].where(
        data_frame_limpio["servicio"].isin(valores_esperados_servicio), pd.NA
    )

    # Limpiar otros campos de texto si existen
    if "ciudad" in data_frame_limpio.columns:
        data_frame_limpio["ciudad"] = (
            data_frame_limpio["ciudad"].astype("string").str.strip().str.lower()
        )
        data_frame_limpio["ciudad"] = data_frame_limpio["ciudad"].where(
            data_frame_limpio["ciudad"].isin(CIUDADES_VALIDAS), pd.NA
        )

    if "canal" in data_frame_limpio.columns:
        data_frame_limpio["canal"] = (
            data_frame_limpio["canal"].astype("string").str.strip().str.lower()
        )
        data_frame_limpio["canal"] = data_frame_limpio["canal"].where(
            data_frame_limpio["canal"].isin(CANALES_VALIDOS), pd.NA
        )

    if "sucursal" in data_frame_limpio.columns:
        data_frame_limpio["sucursal"] = (
            data_frame_limpio["sucursal"].astype("string").str.strip().str.lower()
        )
        data_frame_limpio["sucursal"] = data_frame_limpio["sucursal"].where(
            data_frame_limpio["sucursal"].isin(SUCURSALES_VALIDAS), pd.NA
        )

    if "metodo_pago" in data_frame_limpio.columns:
        data_frame_limpio["metodo_pago"] = (
            data_frame_limpio["metodo_pago"].astype("string").str.strip().str.lower()
        )
        data_frame_limpio["metodo_pago"] = data_frame_limpio["metodo_pago"].where(
            data_frame_limpio["metodo_pago"].isin(METODOS_PAGO_VALIDOS), pd.NA
        )

    # LIMPIEZA DE DATOS NUMERICOS
    # 1. VERIFICAR QUE LOS NUMEROS SI SEAN NUMEROS
    data_frame_limpio["id"] = pd.to_numeric(data_frame_limpio["id"], errors="coerce")
    data_frame_limpio["costo"] = pd.to_numeric(data_frame_limpio["costo"], errors="coerce")

    if "cantidad" in data_frame_limpio.columns:
        data_frame_limpio["cantidad"] = pd.to_numeric(
            data_frame_limpio["cantidad"], errors="coerce"
        )

    # 2. VERIFIQUEMOS LOS VALORES NUMERICOS ESPERADOS
    data_frame_limpio = data_frame_limpio[data_frame_limpio["id"] > 0]
    data_frame_limpio = data_frame_limpio[data_frame_limpio["costo"] >= 5000]

    if "cantidad" in data_frame_limpio.columns:
        data_frame_limpio = data_frame_limpio[data_frame_limpio["cantidad"] > 0]

    # LIMPIEZA DE FECHAS
    # 1. VERIFICAR QUE EL CAMPO SI ES UNA FECHA
    data_frame_limpio["fecha"] = pd.to_datetime(data_frame_limpio["fecha"], errors="coerce")

    # 2. REEMPLAZAR FECHAS QUE NO LLEGAN POR UNA FECHA POR DEFECTO
    fecha_default = pd.to_datetime("2026-01-01")
    data_frame_limpio["fecha"] = data_frame_limpio["fecha"].fillna(fecha_default)

    # NOVEDADES DE DATOS VACIOS
    columnas_obligatorias = ["id", "servicio", "costo", "codigo"]
    antes_dropna = len(data_frame_limpio)
    data_frame_limpio = data_frame_limpio.dropna(subset=columnas_obligatorias)
    reporte["registros_eliminados_por_nulos_obligatorios"] = int(
        antes_dropna - len(data_frame_limpio)
    )

    # ELIMINAR DUPLICADOS
    antes_duplicados = len(data_frame_limpio)
    data_frame_limpio = data_frame_limpio.drop_duplicates()
    reporte["registros_eliminados_por_duplicados"] = int(
        antes_duplicados - len(data_frame_limpio)
    )

    reporte["nulos_finales_por_columna"] = data_frame_limpio.isna().sum().to_dict()
    reporte["tipos_finales"] = {col: str(tipo) for col, tipo in data_frame_limpio.dtypes.items()}
    reporte["registros_finales"] = int(len(data_frame_limpio))

    return data_frame_limpio, reporte


def documentar_transformaciones(reporte, ruta_reporte):
    """Guarda un reporte de transformaciones en formato Markdown."""
    ruta = Path(ruta_reporte)
    ruta.parent.mkdir(parents=True, exist_ok=True)

    lineas = [
        "# Reporte de limpieza de datos",
        "",
        f"Registros iniciales: {reporte['registros_iniciales']}",
        f"Duplicados iniciales detectados: {reporte['duplicados_iniciales']}",
        f"Registros eliminados por nulos obligatorios: {reporte['registros_eliminados_por_nulos_obligatorios']}",
        f"Registros eliminados por duplicados: {reporte['registros_eliminados_por_duplicados']}",
        f"Registros finales: {reporte['registros_finales']}",
        "",
        "Nulos iniciales por columna",
    ]

    for columna, cantidad in reporte["nulos_iniciales_por_columna"].items():
        lineas.append(f"- {columna}: {cantidad}")

    lineas.append("")
    lineas.append("Nulos finales por columna")
    for columna, cantidad in reporte["nulos_finales_por_columna"].items():
        lineas.append(f"- {columna}: {cantidad}")

    lineas.append("")
    lineas.append("ipos finales")
    for columna, tipo in reporte["tipos_finales"].items():
        lineas.append(f"-{columna}: {tipo}")

    ruta.write_text("\n".join(lineas), encoding="utf-8")
