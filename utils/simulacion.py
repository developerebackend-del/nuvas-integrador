import random
from datetime import datetime, timedelta


def generar_simulacion(numero_simulaciones):
    """Genera datos sinteticos con errores controlados para pruebas de limpieza."""
    servicios = [
        {"nombre": "mercado general", "prefijo": "mg", "costo_min": 80000, "costo_max": 250000},
        {"nombre": "aseo hogar", "prefijo": "ah", "costo_min": 20000, "costo_max": 140000},
        {"nombre": "frutas verduras", "prefijo": "fv", "costo_min": 10000, "costo_max": 90000},
    ]
    ciudades = ["bogota", "medellin", "cali", "barranquilla", "bucaramanga"]
    sucursales = ["norte", "centro", "sur", "occidente"]
    canales = ["web", "caja", "app", "domicilio"]
    metodos_pago = ["efectivo", "tarjeta", "transferencia", "billetera digital"]
    fecha_inicio = datetime(2026, 1, 2)

    simulaciones = []
    for _ in range(numero_simulaciones):
        servicio = random.choice(servicios)
        codigo = f"{servicio['prefijo']}{random.randint(1, 399):03d}"

        simulacion = {
            "id": random.randint(1, 5000),
            "servicio": servicio["nombre"],
            "costo": random.randint(servicio["costo_min"], servicio["costo_max"]),
            "codigo": codigo,
            "fecha": fecha_inicio + timedelta(days=random.randint(0, 60)),
            "ciudad": random.choice(ciudades),
            "sucursal": random.choice(sucursales),
            "canal": random.choice(canales),
            "metodo_pago": random.choice(metodos_pago),
            "cantidad": random.randint(1, 30),
        }

        # Inyeccion de errores controlados
        probabilidad_error = random.random()
        if probabilidad_error < 0.12:
            simulacion["id"] = None
        elif probabilidad_error < 0.24:
            simulacion["servicio"] = random.choice(["mecanica", "jardineria"])
        elif probabilidad_error < 0.34:
            simulacion["costo"] = random.choice([0, -10000, None])
        elif probabilidad_error < 0.5:
            simulacion["codigo"] = " " + simulacion["codigo"].upper()
        elif probabilidad_error < 0.62:
            simulacion["fecha"] = None
        elif probabilidad_error < 0.72:
            simulacion["ciudad"] = "  " + simulacion["ciudad"].upper()
        elif probabilidad_error < 0.8:
            simulacion["canal"] = random.choice(["instagram", "whatsapp"])
        elif probabilidad_error < 0.9:
            simulacion["cantidad"] = random.choice([0, -5, None])
        elif probabilidad_error < 0.97:
            simulacion["metodo_pago"] = random.choice(["trueque", "fiado"])

        # Simula duplicados exactos ocasionales para pruebas de HU1.
        if simulaciones and random.random() < 0.05:
            simulacion = random.choice(simulaciones).copy()

        simulaciones.append(simulacion)

    return simulaciones
