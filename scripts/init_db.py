# scripts/init_db.py
import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

# Importar después de configurar el path
from sqlalchemy import create_engine
from app.config.database import Base
from app import init_app  # Importar la aplicación para asegurar que los modelos se registren


def init_db():
    try:
        # Obtener la ruta de la base de datos
        db_path = root_dir / 'facturacion.db'

        print(f"Inicializando base de datos en: {db_path}")

        # Eliminar la base de datos existente si existe
        if db_path.exists():
            print("Eliminando base de datos existente...")
            db_path.unlink()

        # Crear el motor
        engine = create_engine(f"sqlite:///{db_path}")

        # Asegurarse de que los modelos estén registrados
        from app.models import cliente, producto, factura, detalle_factura

        print("Creando tablas...")
        Base.metadata.create_all(bind=engine)

        print("¡Base de datos inicializada correctamente!")
        return True

    except Exception as e:
        print(f"Error al inicializar la base de datos: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Asegurarse de que la aplicación se inicialice para registrar los modelos
    if init_db():
        sys.exit(0)
    else:
        sys.exit(1)