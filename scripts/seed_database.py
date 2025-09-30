#!/usr/bin/env python3
"""
Script para poblar la base de datos con datos de ejemplo.
Incluye 20 productos y 3 clientes.
"""
import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from app.config.database import Base, get_db
from app.models.cliente import Cliente
from app.models.producto import Producto
from datetime import datetime

def create_sample_products(db: Session):
    """Crea productos de ejemplo"""
    productos = [
        {"codigo": "P001", "nombre": "Laptop HP 15", "descripcion": "Laptop HP 15-dw1021la, 15.6\"", "precio": 12999.99, "stock": 15},
        {"codigo": "P002", "nombre": "Mouse Inalámbrico Logitech M185", "descripcion": "Mouse inalámbrico con receptor USB", "precio": 299.99, "stock": 50},
        {"codigo": "P003", "nombre": "Teclado Mecánico Redragon K552", "descripcion": "Teclado mecánico con retroiluminación RGB", "precio": 1499.99, "stock": 25},
        {"codigo": "P004", "nombre": "Monitor Samsung 24\"", "descripcion": "Monitor FHD 1920x1080, 75Hz", "precio": 3499.99, "stock": 12},
        {"codigo": "P005", "nombre": "Disco Duro Externo 1TB", "descripcion": "Disco duro externo portátil USB 3.0", "precio": 1299.99, "stock": 30},
        {"codigo": "P006", "nombre": "Memoria USB 64GB", "descripcion": "USB 3.0, velocidad de hasta 150MB/s", "precio": 249.99, "stock": 100},
        {"codigo": "P007", "nombre": "Audífonos Gamer", "descripcion": "Audífonos con micrófono y luces LED", "precio": 899.99, "stock": 20},
        {"codigo": "P008", "nombre": "Webcam HD 1080p", "descripcion": "Cámara web con micrófono integrado", "precio": 749.99, "stock": 18},
        {"codigo": "P009", "nombre": "Impresora Multifuncional", "descripcion": "Imprime, escanea y copia", "precio": 2499.99, "stock": 8},
        {"codigo": "P010", "nombre": "Router WiFi 6", "descripcion": "Doble banda, velocidad hasta 1800Mbps", "precio": 1599.99, "stock": 15},
        {"codigo": "P011", "nombre": "Tableta Gráfica", "descripcion": "Área activa de 10x6 pulgadas", "precio": 1999.99, "stock": 10},
        {"codigo": "P012", "nombre": "Bocina Bluetooth", "descripcion": "Potencia 20W, resistencia al agua IPX7", "precio": 899.99, "stock": 25},
        {"codigo": "P013", "nombre": "Cargador Inalámbrico 15W", "descripcion": "Carga rápida inalámbrica", "precio": 349.99, "stock": 40},
        {"codigo": "P014", "nombre": "Mouse Pad XXL", "descripcion": "Superficie antideslizante 90x40cm", "precio": 199.99, "stock": 35},
        {"codigo": "P015", "nombre": "Silla Gamer", "descripcion": "Ergonómica con soporte lumbar", "precio": 4599.99, "stock": 5},
        {"codigo": "P016", "nombre": "Mesa para Computadora", "descripcion": "120x60cm, altura ajustable", "precio": 1899.99, "stock": 7},
        {"codigo": "P017", "nombre": "Kit de Limpieza", "descripcion": "Para pantallas y componentes electrónicos", "precio": 149.99, "stock": 60},
        {"codigo": "P018", "nombre": "Hub USB-C", "descripcion": "7 en 1 con HDMI, USB 3.0, SD/TF", "precio": 499.99, "stock": 22},
        {"codigo": "P019", "nombre": "Lámpara LED para Escritorio", "descripcion": "Ajustable, luz cálida y fría", "precio": 299.99, "stock": 18},
        {"codigo": "P020", "nombre": "Funda para Laptop 15.6\"", "descripcion": "Resistente al agua, con correa", "precio": 349.99, "stock": 30},
    ]
    
    for producto_data in productos:
        if not db.query(Producto).filter(Producto.codigo == producto_data["codigo"]).first():
            producto = Producto(**producto_data)
            db.add(producto)
    
    db.commit()
    print(f"Se han creado {len(productos)} productos de ejemplo.")

def create_sample_clients(db: Session):
    """Crea clientes de ejemplo"""
    clientes = [
        {
            "nombre": "Juan",
            "apellido": "Pérez López",
            "dni": "12345678",
            "telefono": "+51987654321",
            "email": "juan.perez@email.com",
            "direccion": "Av. Principal 123, Lima"
        },
        {
            "nombre": "María",
            "apellido": "González Ramírez",
            "dni": "23456789",
            "telefono": "+51987654322",
            "email": "maria.gonzalez@email.com",
            "direccion": "Jr. Libertad 456, Arequipa"
        },
        {
            "nombre": "Carlos",
            "apellido": "Rodríguez Vargas",
            "dni": "34567890",
            "telefono": "+51987654323",
            "email": "carlos.rodriguez@email.com",
            "direccion": "Calle Los Pinos 789, Trujillo"
        }
    ]
    
    for cliente_data in clientes:
        if not db.query(Cliente).filter(Cliente.dni == cliente_data["dni"]).first():
            cliente = Cliente(**cliente_data)
            db.add(cliente)
    
    db.commit()
    print(f"Se han creado {len(clientes)} clientes de ejemplo.")

def main():
    # Crear motor de base de datos
    engine = create_engine('sqlite:///facturacion.db')
    Base.metadata.create_all(bind=engine)
    
    # Crear sesión
    db = Session(engine)
    
    try:
        # Crear datos de ejemplo
        create_sample_products(db)
        create_sample_clients(db)
        print("\n¡Base de datos poblada exitosamente!")
    except Exception as e:
        print(f"Error al poblar la base de datos: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
