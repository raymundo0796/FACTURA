import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.database import Base

# Configuración de la base de datos de prueba
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def test_db():
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    
    # Crear una nueva sesión para la prueba
    db = TestingSessionLocal()
    
    try:
        yield db
    finally:
        # Limpiar después de la prueba
        db.close()
        Base.metadata.drop_all(bind=engine)
