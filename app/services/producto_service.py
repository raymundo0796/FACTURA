from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.producto import Producto
from app.repositories.producto_repository import ProductoRepository


class ProductoService:
    def __init__(self, db: Session):
        self.repository = ProductoRepository(db)

    def get_producto(self, producto_id: int) -> Optional[Producto]:
        """Obtener un producto por su ID"""
        return self.repository.get_by_id(producto_id)

    def get_producto_by_codigo(self, codigo: str) -> Optional[Producto]:
        """Obtener un producto por su código"""
        return self.repository.get_by_codigo(codigo)

    def get_productos(self) -> List[Producto]:
        """Obtener todos los productos"""
        return self.repository.get_all()

    def buscar_productos(self, texto: str) -> List[Producto]:
        """Buscar productos por código o nombre"""
        return self.repository.buscar_por_texto(texto)

    def create_producto(self, producto_data: Dict[str, Any]) -> Producto:
        """Crear un nuevo producto"""
        # Verificar si ya existe un producto con el mismo código
        if self.get_producto_by_codigo(producto_data["codigo"]):
            raise ValueError("Ya existe un producto con este código")

        # Validar que el precio sea positivo
        if producto_data.get("precio", 0) < 0:
            raise ValueError("El precio no puede ser negativo")

        # Validar que el stock no sea negativo
        if producto_data.get("stock", 0) < 0:
            raise ValueError("El stock no puede ser negativo")

        return self.repository.create(producto_data)

    def update_producto(self, producto_id: int, producto_data: Dict[str, Any]) -> Producto:
        """Actualizar un producto existente"""
        producto = self.get_producto(producto_id)
        if not producto:
            raise ValueError("Producto no encontrado")

        # Verificar si se está cambiando el código y si ya existe
        if "codigo" in producto_data and producto_data["codigo"] != producto.codigo:
            if self.get_producto_by_codigo(producto_data["codigo"]):
                raise ValueError("Ya existe un producto con este código")

        # Validar que el precio sea positivo
        if "precio" in producto_data and producto_data["precio"] < 0:
            raise ValueError("El precio no puede ser negativo")

        return self.repository.update(producto, producto_data)

    def delete_producto(self, producto_id: int) -> bool:
        """Eliminar un producto"""
        producto = self.get_producto(producto_id)
        if not producto:
            raise ValueError("Producto no encontrado")

        # Verificar si el producto está siendo usado en alguna factura
        if producto.detalles_factura:
            raise ValueError("No se puede eliminar un producto que está incluido en facturas")

        return self.repository.delete(producto)

    def actualizar_stock(self, producto_id: int, cantidad: int) -> bool:
        """Actualizar el stock de un producto"""
        return self.repository.actualizar_stock(producto_id, cantidad)
