# Tabla de modelos de datos

Este archivo documenta la estructura de los datasets usados en el proyecto.

## 1) Modelo: dataset de entrada (data/raw/data.csv)

| Campo    | Tipo esperado | Requerido | Regla de validacion                   | Ejemplo    |
| -------- | ------------- | --------- | ------------------------------------- | ---------- |
| fecha    | datetime      | Si        | Formato de fecha valido (YYYY-MM-DD)  | 2026-01-01 |
| monto    | float         | Si        | Numero decimal positivo               | 220.5      |
| cliente  | string        | Si        | Texto normalizado (trim y minusculas) | ana        |
| segmento | string        | Si        | Categoria corta (a, b, c, d)          | b          |

## 2) Modelo: dataset sintetico (data/processed/synthetic_data.csv y .json)

| Campo    | Tipo esperado | Requerido | Regla de validacion                         | Ejemplo    |
| -------- | ------------- | --------- | ------------------------------------------- | ---------- |
| id       | int           | Si        | Entero incremental mayor a 0                | 1          |
| fecha    | datetime      | Si        | Fecha valida dentro del rango de simulacion | 2025-10-10 |
| cliente  | string        | Si        | Nombre de cliente simulado                  | diego      |
| segmento | string        | Si        | Categoria simulada (a, b, c, d)             | a          |
| monto    | float         | Si        | Numero decimal entre 50 y 5000              | 4804.91    |
| activo   | bool          | Si        | Valor booleano (True/False)                 | True       |

## 3) Nota de uso

- HU1 usa el modelo de entrada para limpieza (nulos, duplicados, tipos y texto).
- HU2 usa el dataset limpio para exploracion.
- HU3 usa el modelo sintetico para generar y exportar pruebas en CSV y JSON.
