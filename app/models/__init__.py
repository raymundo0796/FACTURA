from app.config.database import Base
from .cliente import Cliente
from .producto import Producto
from .factura import Factura
from .detalle_factura import DetalleFactura

__all__ = ["Base", "Cliente", "Producto", "Factura", "DetalleFactura"]