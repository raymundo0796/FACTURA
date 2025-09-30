# app/models/cliente.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.config.database import Base
from datetime import datetime

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    dni = Column(String(20), unique=True, nullable=False, index=True)
    telefono = Column(String(20))
    email = Column(String(100))
    direccion = Column(String(200))
    fecha_creacion = Column(DateTime, default=datetime.now)

    # Relación con facturas
    facturas = relationship("Factura", back_populates="cliente", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Cliente {self.nombre} {self.apellido}>"