# Proyecto de Analisis de Datos con Pandas

Este proyecto implementa un flujo completo de datos para:

- Simular informacion sintetica con errores controlados.
- Limpiar y estandarizar el dataset.
- Realizar descripcion exploratoria con Pandas.
- Exportar resultados limpios a CSV y JSON.

## Historias de Usuario Cubiertas

### HU 1. Limpieza del set de datos

Como analista de datos, se implemento una rutina de limpieza en `notebook/limpieza.py` que permite:

- Identificar y reportar valores nulos por columna.
- Detectar y eliminar registros duplicados.
- Corregir tipos de datos (numericos y fecha).
- Normalizar texto (espacios y mayusculas/minusculas).
- Documentar transformaciones en un reporte Markdown.

Salida principal:

- `salidas/reporte_limpieza.md`

### HU 2. Descripcion exploratoria con Pandas

Como analista de datos, se implemento la exploracion en `main.py` para:

- Cargar los datos en un DataFrame.
- Visualizar muestras con `head()` y `tail()`.
- Inspeccionar estructura con `info()`.
- Generar estadisticas descriptivas con `describe()`.
- Revisar cantidad de filas, columnas y nombres de variables.
- Identificar columnas numericas y categoricas.

Salida principal:

- `salidas/reporte_exploratorio.json`

### HU 3. Simulacion y exportacion de datos

Como desarrollador de soluciones de datos, se implemento la simulacion en `utils/simulacion.py` para:

- Generar dataset sintetico con al menos 1000 registros (actualmente 1200).
- Incluir varias columnas (id, servicio, costo, codigo, fecha y columnas adicionales).
- Exportar dataset limpio a `.csv` y `.json`.
- Verificar recarga de ambos formatos sin perdida estructural relevante.

Salidas principales:

- `salidas/simulaciones_limpias.csv`
- `salidas/simulaciones_limpias.json`

## Estructura del Proyecto

```text
analisisDatos/
  main.py
  requirements.txt
  README.md
  notebook/
    limpieza.py
  utils/
    simulacion.py
  salidas/
    reporte_exploratorio.json
    reporte_limpieza.md
    simulaciones_limpias.csv
    simulaciones_limpias.json
```

## Preparar Entorno Virtual (Windows PowerShell)

Desde la carpeta raiz del proyecto:

```powershell
# 1) Crear entorno virtual
python -m venv .venv

# 2) Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# 3) Instalar dependencias
pip install -r requirements.txt
```

Si PowerShell bloquea la activacion por politicas de ejecucion:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Despues vuelve a ejecutar:

```powershell
.\.venv\Scripts\Activate.ps1
```

Para desactivar el entorno:

```powershell
deactivate
```

## Ejecutar el Proyecto

Con el entorno activado:

```powershell
python main.py
```

El script:

- Simula 1200 registros.
- Ejecuta exploracion estadistica.
- Limpia y estandariza los datos.
- Exporta resultados a CSV y JSON.
- Genera reportes en la carpeta `salidas/`.

## Validacion Esperada

Al ejecutar correctamente, se imprime un resumen similar a:

- Registros simulados: 1200
- Registros limpios: valor variable segun simulacion
- Validacion exportacion: misma estructura de columnas en CSV y JSON

## Notas

- El generador incluye errores controlados para probar el proceso de limpieza.
- El numero de registros limpios puede cambiar en cada ejecucion por la aleatoriedad de la simulacion.
