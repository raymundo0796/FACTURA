# app/config/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from pathlib import Path

# Obtener la ruta absoluta del directorio base
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'facturacion.db')}"

# Crear el motor de SQLAlchemy
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Crear una fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(SessionLocal)

# Clase base para los modelos
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    """Inicializa la base de datos creando todas las tablas"""
    from app.models import Base
    Base.metadata.create_all(bind=engine)
    print("Base de datos inicializada correctamente")

def get_db():
    """Obtener una sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()