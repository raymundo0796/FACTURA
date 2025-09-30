import pytest
from sqlalchemy.orm import Session
from app.services.cliente_service import ClienteService
from app.models.cliente import Cliente
from datetime import datetime

# Test data
TEST_CLIENTE = {
    "nombre": "Juan",
    "apellido": "Pérez",
    "dni": "12345678",
    "telefono": "+51987654321",
    "email": "juan@example.com",
    "direccion": "Calle Falsa 123"
}

def test_create_cliente(test_db: Session):
    # Arrange
    service = ClienteService(test_db)

    # Act
    cliente = service.create_cliente(TEST_CLIENTE)

    # Assert
    assert cliente is not None
    assert cliente.id is not None
    assert cliente.nombre == "Juan"
    assert cliente.dni == "12345678"
    assert cliente.fecha_creacion is not None

def test_create_duplicate_dni(test_db: Session):
    # Arrange
    service = ClienteService(test_db)
    service.create_cliente(TEST_CLIENTE)

    # Act & Assert
    with pytest.raises(ValueError, match="Ya existe un cliente con este DNI"):
        service.create_cliente(TEST_CLIENTE)

def test_get_cliente_by_id(test_db: Session):
    # Arrange
    service = ClienteService(test_db)
    created = service.create_cliente(TEST_CLIENTE)

    # Act
    found = service.get_cliente(created.id)

    # Assert
    assert found is not None
    assert found.id == created.id
    assert found.nombre == "Juan"

def test_get_nonexistent_cliente(test_db: Session):
    # Arrange
    service = ClienteService(test_db)

    # Act
    found = service.get_cliente(9999)  # ID que no existe

    # Assert
    assert found is None

def test_update_cliente(test_db: Session):
    # Arrange
    service = ClienteService(test_db)
    created = service.create_cliente(TEST_CLIENTE)
    update_data = {"nombre": "Juan Carlos", "telefono": "+51999999999"}

    # Act
    updated = service.update_cliente(created.id, update_data)

    # Assert
    assert updated.nombre == "Juan Carlos"
    assert updated.telefono == "+51999999999"
    assert updated.dni == "12345678"  # No debería cambiar

def test_delete_cliente(test_db: Session):
    # Arrange
    service = ClienteService(test_db)
    created = service.create_cliente(TEST_CLIENTE)

    # Act
    result = service.delete_cliente(created.id)

    # Assert
    assert result is True
    assert service.get_cliente(created.id) is None

def test_buscar_clientes(test_db: Session):
    # Arrange
    service = ClienteService(test_db)
    service.create_cliente(TEST_CLIENTE)

    # Act & Assert
    results = service.buscar_clientes("Juan")
    assert len(results) > 0
    assert any(c.nombre == "Juan" for c in results)

    results = service.buscar_clientes("12345678")
    assert len(results) > 0
    assert any(c.dni == "12345678" for c in results)
