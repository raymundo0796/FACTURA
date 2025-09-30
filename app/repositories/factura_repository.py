from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.factura import Factura
from app.schemas.factura import FacturaCreate, FacturaUpdate


class FacturaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_factura(self, factura_id: int) -> Optional[Factura]:
        """Obtener una factura por su ID"""
        return self.db.query(Factura).filter(Factura.id == factura_id).first()

    def get_factura_by_numero(self, numero_factura: str) -> Optional[Factura]:
        """Obtener una factura por su número de factura"""
        return self.db.query(Factura).filter(Factura.numero_factura == numero_factura).first()

    def get_facturas(self, skip: int = 0, limit: int = 100) -> List[Factura]:
        """Obtener lista de facturas con paginación"""
        return self.db.query(Factura).offset(skip).limit(limit).all()

    def get_facturas_by_cliente(self, cliente_id: int) -> List[Factura]:
        """Obtener facturas por ID de cliente"""
        return self.db.query(Factura).filter(Factura.cliente_id == cliente_id).all()

    def create_factura(self, factura: FacturaCreate) -> Factura:
        """Crear una nueva factura"""
        db_factura = Factura(**factura.dict())
        self.db.add(db_factura)
        self.db.commit()
        self.db.refresh(db_factura)
        return db_factura

    def update_factura(self, factura_id: int, factura: FacturaUpdate) -> Optional[Factura]:
        """Actualizar una factura existente"""
        db_factura = self.get_factura(factura_id)
        if db_factura:
            update_data = factura.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_factura, key, value)
            self.db.commit()
            self.db.refresh(db_factura)
        return db_factura

    def delete_factura(self, factura_id: int) -> bool:
        """Eliminar una factura por su ID"""
        db_factura = self.get_factura(factura_id)
        if db_factura:
            self.db.delete(db_factura)
            self.db.commit()
            return True
        return False

    def get_total_facturas(self) -> int:
        """Obtener el número total de facturas"""
        return self.db.query(Factura).count()
