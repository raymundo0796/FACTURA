from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class DetalleFacturaBase(BaseModel):
    producto_id: int
    cantidad: int = Field(..., gt=0, description="La cantidad debe ser mayor a cero")
    precio_unitario: float = Field(..., gt=0, description="El precio unitario debe ser mayor a cero")


class DetalleFacturaCreate(DetalleFacturaBase):
    pass


class DetalleFactura(DetalleFacturaBase):
    id: int
    subtotal: float

    class Config:
        orm_mode = True


class FacturaBase(BaseModel):
    cliente_id: int
    numero_factura: str
    fecha_emision: datetime = Field(default_factory=datetime.now)
    subtotal: float = 0.0
    impuesto: float = 0.0
    total: float = 0.0
    estado: str = "PENDIENTE"  # PENDIENTE, PAGADA, ANULADA


class FacturaCreate(FacturaBase):
    detalles: List[DetalleFacturaCreate] = Field(..., min_items=1, description="La factura debe tener al menos un detalle")


class FacturaUpdate(BaseModel):
    estado: Optional[str] = None
    impuesto: Optional[float] = None


class Factura(FacturaBase):
    id: int
    fecha_creacion: datetime
    detalles: List[DetalleFactura] = []

    class Config:
        orm_mode = True
