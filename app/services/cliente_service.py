# app/services/cliente_service.py
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.cliente import Cliente
from app.repositories.cliente_repository import ClienteRepository


class ClienteService:
    def __init__(self, db: Session):
        self.repository = ClienteRepository(db)

    def get_cliente(self, cliente_id: int) -> Optional[Cliente]:
        """Obtener un cliente por su ID"""
        return self.repository.get_by_id(cliente_id)

    def get_cliente_by_dni(self, dni: str) -> Optional[Cliente]:
        """Obtener un cliente por su DNI"""
        return self.repository.get_by_dni(dni)

    def get_clientes(self) -> List[Cliente]:
        """Obtener todos los clientes"""
        return self.repository.get_all()

    def create_cliente(self, cliente_data: Dict[str, Any]) -> Cliente:
        """Crear un nuevo cliente"""
        # Verificar si ya existe un cliente con el mismo DNI
        if self.get_cliente_by_dni(cliente_data["dni"]):
            raise ValueError("Ya existe un cliente con este DNI")

        return self.repository.create(cliente_data)

    def update_cliente(self, cliente_id: int, cliente_data: Dict[str, Any]) -> Cliente:
        """Actualizar un cliente existente"""
        cliente = self.get_cliente(cliente_id)
        if not cliente:
            raise ValueError("Cliente no encontrado")

        # Verificar si el DNI ya está en uso por otro cliente
        if "dni" in cliente_data:
            existing_cliente = self.get_cliente_by_dni(cliente_data["dni"])
            if existing_cliente and existing_cliente.id != cliente_id:
                raise ValueError("El DNI ya está en uso por otro cliente")

        return self.repository.update(cliente, cliente_data)

    def delete_cliente(self, cliente_id: int) -> bool:
        """Eliminar un cliente por su ID"""
        cliente = self.get_cliente(cliente_id)
        if not cliente:
            raise ValueError("Cliente no encontrado")
            
        return self.repository.delete(cliente_id)
        
    def buscar_clientes(self, texto: str) -> list[Cliente]:
        """Buscar clientes por nombre, apellido o DNI"""
        return self.repository.buscar_por_texto(texto)