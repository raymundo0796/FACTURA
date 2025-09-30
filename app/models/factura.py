from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base


class Factura(Base):
    __tablename__ = "facturas"

    id = Column(Integer, primary_key=True, index=True)
    numero_factura = Column(String(50), unique=True, nullable=False, index=True)
    fecha_emision = Column(DateTime, nullable=False, server_default="CURRENT_TIMESTAMP")
    subtotal = Column(Float, nullable=False, default=0.0)
    impuesto = Column(Float, nullable=False, default=0.0)
    total = Column(Float, nullable=False, default=0.0)
    estado = Column(String(20), default="PENDIENTE")  # PENDIENTE, PAGADA, ANULADA

    # Claves foráneas
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)

    # Relaciones
    cliente = relationship("Cliente", back_populates="facturas")
    detalles = relationship("DetalleFactura", back_populates="factura", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Factura {self.numero_factura}>"