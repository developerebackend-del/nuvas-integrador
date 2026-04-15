# Nuvas Integrador

Proyecto de análisis de datos en Python orientado a buenas prácticas de ingeniería.

Este repositorio implementa tres historias de usuario:

- HU1: limpieza de datasets (nulos, duplicados, tipos y normalización de texto).
- HU2: descripción exploratoria con Pandas (head, tail, info, describe y clasificación de columnas).
- HU3: simulación y exportación de datos a CSV y JSON.

## Objetivo

Preparar datos confiables para análisis y generar una descripción exploratoria clara del dataset, manteniendo una estructura mantenible y testeable.

## Estructura del proyecto

```text
nuvas-integrador/
	data/
		raw/
			data.csv
	src/nuvas_integrador/
		config.py
		main.py
		data/
			loader.py
			simulator.py
		models/
			dataset_model.py
			synthetic_model.py
		processing/
			cleaning.py
			explorer.py
	requirements.txt
	pyproject.toml
	pytest.ini
```

## Requisitos

- Python 3.11+
- pip

## Configuración del entorno

Windows (PowerShell):

```powershell
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
```

Si PowerShell bloquea la activación del entorno, puedes usar el ejecutable directo:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Ejecución

```powershell
python -m nuvas_integrador.main
```

## Testing

Las pruebas automaticas estan pausadas temporalmente.

## Cobertura funcional

## Lo Que Se Implementó

- Estructura por carpetas simple y separada: `data`, `models`, `processing` y `main.py`.
- Flujo principal en consola para ejecutar HU1, HU2 y HU3 en un solo comando.
- Modelos de datos con `dataclass` en `src/nuvas_integrador/models`.
- Documento de tabla de modelos en `docs/tabla_modelos.md`.

### HU1. Limpieza del set de datos

- Identificación y reporte de nulos por columna.
- Detección y eliminación de registros duplicados.
- Corrección de tipos de datos con `mapeo_tipos` (fechas, numéricos, texto).
- Normalización de texto (trim, espacios internos y minúsculas).
- Documentación de transformaciones en `reporte["transformaciones"]`.

### HU2. Descripción exploratoria con Pandas

- Carga del dataset en DataFrame con `load_csv`.
- Visualización de muestras con `head()` y `tail()`.
- Inspección de estructura con `info()`.
- Estadísticas descriptivas con `describe()`.
- Revisión de cantidad de filas, columnas y nombres de variables.
- Identificación de columnas numéricas y categóricas.

### HU3. Simulación y exportación de datos

- Generación de dataset sintético en Python con al menos 1000 registros.
- Dataset con varias columnas (`id`, `fecha`, `cliente`, `segmento`, `monto`, `activo`).
- Exportación correcta a CSV en `data/processed/synthetic_data.csv`.
- Exportación correcta a JSON en `data/processed/synthetic_data.json`.
- Validación en ejecución para confirmar que CSV/JSON conservan estructura y tamaño del dataset original.

## Flujo Git para subir a una rama

Ejemplo para trabajar en una rama de funcionalidad:

```powershell
# 1) Verifica estado actual
git status

# 2) Crea y cámbiate a una rama nueva
git checkout -b feature/hu1-hu2

# 3) Agrega cambios
git add .

# 4) Crea commit
git commit -m "feat: implementar HU1 y HU2 con tests"

# 5) Sube la rama al remoto
git push -u origin feature/hu1-hu2
```

Después, crea el Pull Request desde esa rama hacia `main` en GitHub.
