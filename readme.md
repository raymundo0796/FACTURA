# Sistema de Facturación

Sistema de gestión de facturas desarrollado con Python, PyQt6 y SQLAlchemy.

## 🚀 Características Principales

- Gestión de clientes
- Gestión de productos
- Creación y edición de facturas
- Cálculo automático de totales e impuestos
- Interfaz gráfica intuitiva

## 🛠️ Requisitos Previos

- Python 3.9 o superior
- pip (gestor de paquetes de Python)
- SQLite3 (incluido en Python)

## 🚀 Configuración del Entorno

1. Clona el repositorio:
   ```bash
   git clone [URL_DEL_REPOSITORIO]
   cd FACTURA
   ```

2. Crea y activa un entorno virtual (recomendado):
   ```bash
   # En macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   
   # En Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## 🏗️ Configuración de la Base de Datos

1. Inicializa la base de datos y crea las tablas necesarias:
   ```bash
   python -m scripts.init_db
   ```

   Esto creará un archivo `facturacion.db` en el directorio raíz.

2. Para poblar la base de datos con datos de ejemplo (20 productos y 3 clientes), ejecuta:
   ```bash
   python -m scripts.seed_database
   ```
   
   Este comando creará:
   - 20 productos de ejemplo (electrónicos y accesorios)
   - 3 clientes de ejemplo con información de contacto

   > 💡 **Nota**: Este paso es opcional pero recomendado para pruebas.

## 🚀 Ejecutar la Aplicación

```bash
python run.py
```

## 🧪 Ejecutar Pruebas

Para ejecutar las pruebas unitarias:

```bash
pytest tests/
```

Para ver el reporte de cobertura:

```bash
pytest --cov=app tests/
```

## 🏗️ Estructura del Proyecto

```
FACTURA/
├── app/
│   ├── config/         # Configuración de la base de datos
│   ├── models/         # Modelos de datos
│   ├── repositories/   # Acceso a datos
│   ├── schemas/        # Esquemas Pydantic
│   └── services/       # Lógica de negocio
│   └── views/          # Interfaces de usuario
├── scripts/           # Scripts de utilidad
├── tests/             # Pruebas unitarias
├── .env.example       # Variables de entorno de ejemplo
├── requirements.txt   # Dependencias
└── run.py            # Punto de entrada de la aplicación
```

## 🛠️ Desarrollo

### Formateo de Código

```bash
black .
isort .
```

### Convenciones de Commits

- Usa mensajes descriptivos
- Agrupa cambios relacionados en commits lógicos
- Sigue el formato: `tipo(ámbito): descripción breve`

### Tipos de Commits

- `feat`: Nueva característica
- `fix`: Corrección de errores
- `docs`: Cambios en la documentación
- `style`: Cambios de formato (puntuación, etc.)
- `refactor`: Cambios que no corrigen errores ni agregan características
- `test`: Agregar o corregir pruebas
- `chore`: Cambios en el proceso de compilación o herramientas auxiliares

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor, lee las [pautas de contribución](CONTRIBUTING.md) antes de enviar pull requests.
