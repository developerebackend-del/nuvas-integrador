from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class RegistroSintetico:
    """Modelo simple del dataset sintetico (HU3)."""

    id: int
    fecha: datetime
    cliente: str
    segmento: str
    monto: float
    activo: bool
