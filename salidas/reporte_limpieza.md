# Reporte de limpieza de datos

- Registros iniciales: 1200
- Duplicados iniciales detectados: 51
- Registros eliminados por nulos obligatorios: 128
- Registros eliminados por duplicados: 28
- Registros finales: 650

## Nulos iniciales por columna
- id: 155
- servicio: 0
- costo: 47
- codigo: 0
- fecha: 128
- ciudad: 0
- sucursal: 0
- canal: 0
- metodo_pago: 0
- cantidad: 34

## Nulos finales por columna
- id: 0
- servicio: 0
- costo: 0
- codigo: 0
- fecha: 0
- ciudad: 0
- sucursal: 0
- canal: 99
- metodo_pago: 87
- cantidad: 0

## Tipos finales
- id: float64
- servicio: string
- costo: float64
- codigo: string
- fecha: datetime64[us]
- ciudad: string
- sucursal: string
- canal: string
- metodo_pago: string
- cantidad: float64