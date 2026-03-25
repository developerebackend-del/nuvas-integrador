# Nuvas Integrador

Proyecto de análisis de datos en Python orientado a buenas prácticas de ingeniería.

Este repositorio implementa dos historias de usuario:

- HU1: limpieza de datasets (nulos, duplicados, tipos y normalización de texto).
- HU2: descripción exploratoria con Pandas (head, tail, info, describe y clasificación de columnas).

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
		processing/
			cleaning.py
			explorer.py
	tests/
		test_cleaning.py
		test_explorer.py
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

```powershell
python -m pytest -q
```

## Cobertura funcional

### HU1. Limpieza del set de datos

- Identificación y reporte de nulos por columna.
- Detección y eliminación de registros duplicados.
- Corrección de tipos de datos con `type_mapping` (fechas, numéricos, texto).
- Normalización de texto (trim, espacios internos y minúsculas).
- Documentación de transformaciones en `report["transformations"]`.

### HU2. Descripción exploratoria con Pandas

- Carga del dataset en DataFrame con `load_csv`.
- Visualización de muestras con `head()` y `tail()`.
- Inspección de estructura con `info()`.
- Estadísticas descriptivas con `describe()`.
- Revisión de cantidad de filas, columnas y nombres de variables.
- Identificación de columnas numéricas y categóricas.

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
