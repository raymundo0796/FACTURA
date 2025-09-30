from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.factura import Factura
from app.models.detalle_factura import DetalleFactura
from app.models.producto import Producto
from app.repositories.factura_repository import FacturaRepository
from app.repositories.producto_repository import ProductoRepository
from app.repositories.cliente_repository import ClienteRepository


class FacturaService:
    def __init__(self, db: Session):
        self.db = db
        self.factura_repo = FacturaRepository(db)
        self.producto_repo = ProductoRepository(db)
        self.cliente_repo = ClienteRepository(db)

    def get_factura(self, factura_id: int) -> Optional[Factura]:
        return self.factura_repo.get_factura(factura_id)

    def get_facturas(self) -> List[Factura]:
        return self.factura_repo.get_facturas()

    def buscar_facturas(self, termino: str) -> List[Factura]:
        return self.factura_repo.buscar(termino)

    def create_factura(self, factura_data: Dict[str, Any]) -> Factura:
        # Verificar que el cliente existe
        if not self.cliente_repo.get_by_id(factura_data['cliente_id']):
            raise ValueError(f"Cliente con ID {factura_data['cliente_id']} no encontrado")

        # Generar número de factura único (año-mes-día-numero)
        from datetime import datetime
        fecha_actual = datetime.now()
        prefijo = fecha_actual.strftime("%Y%m%d")
        
        # Obtener el último número de factura del día
        ultima_factura = self.db.query(Factura).filter(
            Factura.numero_factura.like(f"{prefijo}%")  
        ).order_by(Factura.id.desc()).first()
        
        if ultima_factura:
            ultimo_numero = int(ultima_factura.numero_factura.split('-')[-1])
            nuevo_numero = f"{prefijo}-{ultimo_numero + 1:04d}"
        else:
            nuevo_numero = f"{prefijo}-0001"

        # Crear la factura con el número generado
        factura = Factura(
            numero_factura=nuevo_numero,
            cliente_id=factura_data['cliente_id'],
            fecha_emision=fecha_actual,
            estado=factura_data.get('estado', 'PENDIENTE'),
            subtotal=0.0,
            impuesto=factura_data.get('impuesto', 0.0),
            total=0.0
        )
        
        # Guardar la factura para obtener el ID
        self.db.add(factura)
        self.db.flush()
        
        # Procesar detalles de la factura
        total = 0.0
        for detalle_data in factura_data.get('detalles', []):
            producto = self.producto_repo.get_by_id(detalle_data['producto_id'])
            if not producto:
                raise ValueError(f"Producto con ID {detalle_data['producto_id']} no encontrado")
            
            cantidad = detalle_data['cantidad']
            if producto.stock < cantidad:
                raise ValueError(f"Stock insuficiente para el producto {producto.nombre}")
            
            # Actualizar stock
            producto.stock -= cantidad
            
            # Calcular subtotal
            subtotal = cantidad * detalle_data['precio_unitario']
            total += subtotal
            
            # Crear detalle de factura
            detalle = DetalleFactura(
                factura_id=factura.id,
                producto_id=producto.id,
                cantidad=cantidad,
                precio_unitario=detalle_data['precio_unitario'],
                subtotal=subtotal
            )
            self.db.add(detalle)
        
        # Actualizar totales de la factura
        impuesto = total * (factura.impuesto / 100)
        factura.subtotal = total
        factura.total = total + impuesto
        
        # Guardar cambios
        self.db.commit()
        self.db.refresh(factura)
        
        return factura

    def update_factura(self, factura_id: int, factura_data: Dict[str, Any]) -> Optional[Factura]:
        factura = self.factura_repo.get(factura_id)
        if not factura:
            return None
            
        # Actualizar campos básicos
        if 'estado' in factura_data:
            factura.estado = factura_data['estado']
            
        # Actualizar total si es necesario
        if 'total' in factura_data:
            factura.total = factura_data['total']
            
        self.db.commit()
        self.db.refresh(factura)
        return factura

    def delete_factura(self, factura_id: int) -> bool:
        factura = self.factura_repo.get(factura_id)
        if not factura:
            return False
            
        # Revertir stock de productos
        for detalle in factura.detalles:
            producto = self.producto_repo.get(detalle.producto_id)
            if producto:
                producto.stock += detalle.cantidad
                
        # Eliminar factura
        self.db.delete(factura)
        self.db.commit()
        return True
