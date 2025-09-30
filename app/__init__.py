from .config.database import init_db

# Importar modelos para que se registren con SQLAlchemy
from .models import cliente, producto, factura, detalle_factura

def init_app():
    """Inicializa la aplicación y la base de datos"""
    # Inicializar la base de datos
    init_db()
    print("Aplicación inicializada correctamente")