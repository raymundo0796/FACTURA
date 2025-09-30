import pytest
from unittest.mock import Mock, create_autospec
from sqlalchemy.orm import Session
from datetime import datetime

from app.services.cliente_service import ClienteService
from app.models.cliente import Cliente

# Fixture para el mock de la sesión de base de datos
@pytest.fixture
def mock_db_session():
    return create_autospec(Session, instance=True)

# Fixture para el servicio con mocks
@pytest.fixture
def cliente_service(mock_db_session):
    return ClienteService(mock_db_session)

def test_create_cliente_success(cliente_service, mock_db_session):
    # Arrange
    cliente_data = {
        "nombre": "Juan",
        "apellido": "Pérez",
        "dni": "12345678",
        "telefono": "+51987654321",
        "email": "juan@example.com",
        "direccion": "Calle Falsa 123"
    }
    
    # Configurar el mock para simular que no existe un cliente con el mismo DNI
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    
    # Mock para el objeto Cliente que se creará
    cliente_mock = Mock()
    cliente_mock.id = 1
    cliente_mock.nombre = "Juan"
    cliente_mock.apellido = "Pérez"
    cliente_mock.dni = "12345678"
    mock_db_session.add.return_value = cliente_mock
    
    # Act
    result = cliente_service.create_cliente(cliente_data)
    
    # Assert
    assert result.nombre == "Juan"
    assert result.apellido == "Pérez"
    assert result.dni == "12345678"
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()

def test_create_cliente_duplicate_dni(cliente_service, mock_db_session):
    # Arrange
    cliente_data = {
        "nombre": "Juan",
        "apellido": "Pérez",
        "dni": "12345678",
        "telefono": "+51987654321"
    }
    
    # Configurar el mock para simular que ya existe un cliente con el mismo DNI
    mock_db_session.query.return_value.filter.return_value.first.return_value = Cliente(
        id=1,
        dni="12345678",
        nombre="Otro",
        apellido="Usuario"
    )
    
    # Act & Assert
    with pytest.raises(ValueError, match="Ya existe un cliente con este DNI"):
        cliente_service.create_cliente(cliente_data)

def test_get_cliente(cliente_service, mock_db_session):
    # Arrange
    cliente_mock = Cliente(
        id=1,
        nombre="Juan",
        apellido="Pérez",
        dni="12345678",
        telefono="+51987654321"
    )
    mock_db_session.query.return_value.filter.return_value.first.return_value = cliente_mock
    
    # Act
    result = cliente_service.get_cliente(1)
    
    # Assert
    assert result.id == 1
    assert result.nombre == "Juan"
    mock_db_session.query.return_value.filter.assert_called_once()

def test_update_cliente(cliente_service, mock_db_session):
    # Arrange
    cliente_existente = Cliente(
        id=1,
        nombre="Juan",
        apellido="Pérez",
        dni="12345678",
        telefono="+51987654321"
    )
    
    update_data = {
        "telefono": "+51999999999",
        "email": "nuevo@email.com"
    }
    
    mock_db_session.query.return_value.filter.return_value.first.return_value = cliente_existente
    
    # Act
    result = cliente_service.update_cliente(1, update_data)
    
    # Assert
    assert result.telefono == "+51999999999"
    assert result.email == "nuevo@email.com"
    assert result.dni == "12345678"  # No debería cambiar
    mock_db_session.commit.assert_called_once()

def test_delete_cliente(cliente_service, mock_db_session):
    # Arrange
    cliente_mock = Mock()
    mock_db_session.query.return_value.filter.return_value.first.return_value = cliente_mock
    
    # Act
    result = cliente_service.delete_cliente(1)
    
    # Assert
    assert result is True
    mock_db_session.delete.assert_called_once_with(cliente_mock)
    mock_db_session.commit.assert_called_once()

def test_buscar_clientes_por_nombre(cliente_service, mock_db_session):
    # Arrange
    clientes_mock = [
        Cliente(id=1, nombre="Juan", apellido="Pérez", dni="12345678"),
        Cliente(id=2, nombre="Juan", apellido="Gómez", dni="87654321")
    ]
    
    # Configurar la cadena de mocks para incluir order_by()
    mock_query = mock_db_session.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_order = mock_filter.order_by.return_value
    mock_order.all.return_value = clientes_mock
    
    # Act
    resultados = cliente_service.buscar_clientes("Juan")
    
    # Assert
    assert len(resultados) == 2
    assert all(cliente.nombre == "Juan" for cliente in resultados)
    mock_filter.order_by.assert_called_once()

def test_buscar_clientes_por_dni(cliente_service, mock_db_session):
    # Arrange
    cliente_mock = Cliente(id=1, nombre="Juan", apellido="Pérez", dni="12345678")
    
    # Configurar la cadena de mocks para incluir order_by()
    mock_query = mock_db_session.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_order = mock_filter.order_by.return_value
    mock_order.all.return_value = [cliente_mock]
    
    # Act
    resultados = cliente_service.buscar_clientes("12345678")
    
    # Assert
    assert len(resultados) == 1
    assert resultados[0].dni == "12345678"
    mock_filter.order_by.assert_called_once()
