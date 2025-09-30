from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.producto import Producto
from .base_repository import BaseRepository


class ProductoRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(Producto, db)

    def get_by_codigo(self, codigo: str) -> Optional[Producto]:
        """Obtener un producto por su código"""
        return self.db.query(Producto).filter(Producto.codigo == codigo).first()
        
    def buscar_por_texto(self, texto: str) -> List[Producto]:
        """Buscar productos por código o nombre"""
        if not texto:
            return self.get_all()
            
        texto_busqueda = f"%{texto.lower()}%"
        return (
            self.db.query(Producto)
            .filter(
                (Producto.codigo.ilike(texto_busqueda)) |
                (Producto.nombre.ilike(texto_busqueda))
            )
            .order_by(Producto.nombre)
            .all()
        )
        
    def actualizar_stock(self, producto_id: int, cantidad: int) -> bool:
        """Actualizar el stock de un producto"""
        producto = self.get_by_id(producto_id)
        if not producto:
            return False
            
        producto.stock += cantidad
        self.db.commit()
        self.db.refresh(producto)
        return True
