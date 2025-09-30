# run.py
import sys
from PyQt6.QtWidgets import QApplication
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.views.main_window import MainWindow
from app.config.database import Base, engine

def init_db():
    """Inicializar la base de datos y crear tablas si no existen"""
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

def main():
    # Inicializar la base de datos y obtener sesión
    db = init_db()

    # Crear la aplicación Qt
    app = QApplication(sys.argv)

    # Crear y mostrar la ventana principal
    window = MainWindow(db)
    window.show()

    # Ejecutar el bucle de eventos
    sys.exit(app.exec())


if __name__ == "__main__":
    main()