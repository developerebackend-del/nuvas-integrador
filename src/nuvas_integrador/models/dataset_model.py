from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class RegistroEntrada:
    """Modelo simple del dataset de entrada (data/raw/data.csv)."""

    fecha: datetime
    monto: float
    cliente: str
    segmento: str
