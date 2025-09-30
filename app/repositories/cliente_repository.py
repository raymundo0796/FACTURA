from typing import Optional
from sqlalchemy.orm import Session
from app.models.cliente import Cliente
from .base_repository import BaseRepository


class ClienteRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(Cliente, db)

    def get_by_dni(self, dni: str) -> Optional[Cliente]:
        """Obtener un cliente por su DNI"""
        return self.db.query(Cliente).filter(Cliente.dni == dni).first()
        
    def buscar_por_texto(self, texto: str) -> list[Cliente]:
        """Buscar clientes por nombre, apellido o DNI"""
        if not texto:
            return self.get_all()
            
        texto_busqueda = f"%{texto.lower()}%"
        return (
            self.db.query(Cliente)
            .filter(
                (Cliente.nombre.ilike(texto_busqueda)) |
                (Cliente.apellido.ilike(texto_busqueda)) |
                (Cliente.dni.ilike(texto_busqueda))
            )
            .order_by(Cliente.apellido, Cliente.nombre)
            .all()
        )