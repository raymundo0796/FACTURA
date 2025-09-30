from PyQt6.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit, QMessageBox, QDialog,
    QFormLayout, QDialogButtonBox, QComboBox, QDateEdit, QLabel, QDoubleSpinBox, QSpinBox
)
from PyQt6.QtCore import Qt, QSize, QDate
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.config.database import Base, get_db
from app.services.cliente_service import ClienteService
from app.services.producto_service import ProductoService
from app.services.factura_service import FacturaService
from app.models.cliente import Cliente
from app.models.producto import Producto
from app.models.factura import Factura
from app.views.factura_dialog import FacturaDialog

class MainWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Sistema de Facturación")
        self.setGeometry(100, 100, 1000, 700)

        # Inicializar servicios
        self.cliente_service = ClienteService(db)
        self.producto_service = ProductoService(db)
        self.factura_service = FacturaService(db)
        
        self.setup_ui()
        self.cargar_clientes()
        self.cargar_productos()
        self.cargar_facturas()

    def setup_ui(self):
        """Configurar la interfaz de usuario principal"""
        self.setWindowTitle("Sistema de Facturación")
        self.setMinimumSize(1000, 600)

        # Crear widget central y layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Crear pestañas
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # Pestaña de Clientes
        self.setup_clientes_tab()
        
        # Pestaña de Productos
        self.setup_productos_tab()
        
        # Pestaña de Facturas
        self.setup_facturas_tab()
        
        # Aplicar estilos
        self.apply_styles()

    def setup_clientes_tab(self):
        # Pestaña de Clientes
        self.cliente_tab = QWidget()
        self.tabs.addTab(self.cliente_tab, "Clientes")

        # Configurar el layout de la pestaña de Clientes
        cliente_layout = QVBoxLayout(self.cliente_tab)
        cliente_layout.setContentsMargins(10, 10, 10, 10)
        cliente_layout.setSpacing(10)

        # Barra de búsqueda y botones
        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.setSpacing(10)
        
        self.buscar_input = QLineEdit()
        self.buscar_input.setPlaceholderText("Buscar por nombre o DNI...")
        self.buscar_input.setMinimumWidth(300)
        self.buscar_input.setMaximumWidth(400)
        
        btn_agregar = QPushButton("Nuevo Cliente")
        btn_editar = QPushButton("Editar")
        btn_eliminar = QPushButton("Eliminar")
        
        # Establecer tamaños fijos para los botones
        for btn in [btn_agregar, btn_editar, btn_eliminar]:
            btn.setFixedWidth(120)
            btn.setMinimumHeight(30)
        
        search_layout.addWidget(self.buscar_input, alignment=Qt.AlignmentFlag.AlignLeft)
        search_layout.addStretch()
        search_layout.addWidget(btn_editar)
        search_layout.addWidget(btn_eliminar)
        search_layout.addWidget(btn_agregar)
        
        cliente_layout.addWidget(search_container)

        # Tabla de clientes
        self.tabla_clientes = QTableWidget()
        self.tabla_clientes.setColumnCount(4)
        self.tabla_clientes.setHorizontalHeaderLabels(['ID', 'Nombre', 'Email', 'Teléfono'])
        header = self.tabla_clientes.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.tabla_clientes.verticalHeader().setVisible(False)
        self.tabla_clientes.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla_clientes.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        
        cliente_layout.addWidget(self.tabla_clientes, 1)  # El 1 hace que la tabla ocupe el espacio restante

        # Conectar señales
        btn_agregar.clicked.connect(self.agregar_cliente)
        btn_editar.clicked.connect(self.editar_cliente)
        btn_eliminar.clicked.connect(self.eliminar_cliente)
        self.buscar_input.textChanged.connect(self.buscar_cliente)

    def setup_productos_tab(self):
        # Pestaña de Productos
        self.producto_tab = QWidget()
        self.tabs.addTab(self.producto_tab, "Productos")

        # Configurar el layout de la pestaña de Productos
        producto_layout = QVBoxLayout(self.producto_tab)
        producto_layout.setContentsMargins(10, 10, 10, 10)
        producto_layout.setSpacing(10)

        # Barra de búsqueda y botones
        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.setSpacing(10)
        
        self.buscar_producto_input = QLineEdit()
        self.buscar_producto_input.setPlaceholderText("Buscar por nombre o código...")
        self.buscar_producto_input.setMinimumWidth(300)
        self.buscar_producto_input.setMaximumWidth(400)
        
        btn_agregar_producto = QPushButton("Nuevo Producto")
        btn_editar_producto = QPushButton("Editar")
        btn_eliminar_producto = QPushButton("Eliminar")
        
        # Establecer tamaños fijos para los botones
        for btn in [btn_agregar_producto, btn_editar_producto, btn_eliminar_producto]:
            btn.setFixedWidth(120)
            btn.setMinimumHeight(30)
        
        search_layout.addWidget(self.buscar_producto_input, alignment=Qt.AlignmentFlag.AlignLeft)
        search_layout.addStretch()
        search_layout.addWidget(btn_editar_producto)
        search_layout.addWidget(btn_eliminar_producto)
        search_layout.addWidget(btn_agregar_producto)
        
        producto_layout.addWidget(search_container)

        # Tabla de productos
        self.tabla_productos = QTableWidget()
        self.tabla_productos.setColumnCount(4)
        self.tabla_productos.setHorizontalHeaderLabels(['ID', 'Nombre', 'Código', 'Precio'])
        header = self.tabla_productos.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.tabla_productos.verticalHeader().setVisible(False)
        self.tabla_productos.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla_productos.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        
        producto_layout.addWidget(self.tabla_productos, 1)  # El 1 hace que la tabla ocupe el espacio restante

        # Conectar señales
        btn_agregar_producto.clicked.connect(self.agregar_producto)
        btn_editar_producto.clicked.connect(self.editar_producto)
        btn_eliminar_producto.clicked.connect(self.eliminar_producto)
        self.buscar_producto_input.textChanged.connect(self.buscar_producto)

    def setup_facturas_tab(self):
        # Pestaña de Facturas
        self.factura_tab = QWidget()
        self.tabs.addTab(self.factura_tab, "Facturas")

        # Configurar el layout de la pestaña de Facturas
        factura_layout = QVBoxLayout(self.factura_tab)
        factura_layout.setContentsMargins(10, 10, 10, 10)
        factura_layout.setSpacing(10)

        # Barra de búsqueda y botones
        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.setSpacing(10)
        
        self.buscar_factura_input = QLineEdit()
        self.buscar_factura_input.setPlaceholderText("Buscar por número o fecha...")
        self.buscar_factura_input.setMinimumWidth(300)
        self.buscar_factura_input.setMaximumWidth(400)
        
        btn_agregar_factura = QPushButton("Nueva Factura")
        btn_editar_factura = QPushButton("Editar")
        btn_eliminar_factura = QPushButton("Eliminar")
        
        # Establecer tamaños fijos para los botones
        for btn in [btn_agregar_factura, btn_editar_factura, btn_eliminar_factura]:
            btn.setFixedWidth(120)
            btn.setMinimumHeight(30)
        
        search_layout.addWidget(self.buscar_factura_input, alignment=Qt.AlignmentFlag.AlignLeft)
        search_layout.addStretch()
        search_layout.addWidget(btn_editar_factura)
        search_layout.addWidget(btn_eliminar_factura)
        search_layout.addWidget(btn_agregar_factura)
        
        factura_layout.addWidget(search_container)

        # Tabla de facturas
        self.tabla_facturas = QTableWidget()
        self.tabla_facturas.setColumnCount(4)
        self.tabla_facturas.setHorizontalHeaderLabels(['ID', 'Número', 'Fecha', 'Total'])
        header = self.tabla_facturas.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.tabla_facturas.verticalHeader().setVisible(False)
        self.tabla_facturas.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla_facturas.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        
        factura_layout.addWidget(self.tabla_facturas, 1)  # El 1 hace que la tabla ocupe el espacio restante

        # Conectar señales
        btn_agregar_factura.clicked.connect(self.agregar_factura)
        btn_editar_factura.clicked.connect(self.editar_factura)
        btn_eliminar_factura.clicked.connect(self.eliminar_factura)
        self.buscar_factura_input.textChanged.connect(self.buscar_factura)

    def apply_styles(self):
        """Aplicar estilos a la interfaz de usuario"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f7fa;
            }
            QTabWidget::pane {
                border: 1px solid #d1d5db;
                border-radius: 6px;
                margin: 5px;
                padding: 0px;
                background: white;
            }
            QTabBar::tab {
                background: #e5e7eb;
                border: 1px solid #d1d5db;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 8px 16px;
                margin-right: 4px;
                color: #1f2937;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom: 1px solid white;
                margin-bottom: -1px;
                color: #1f2937;
            }
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton:disabled {
                background-color: #93c5fd;
            }
            QLineEdit, QComboBox, QTextEdit {
                background-color: white;
                color: #1f2937;
                border: 1px solid #d1d5db;
                border-radius: 4px;
                padding: 6px 8px;
                min-height: 30px;
            }
            QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
                border: 1px solid #3b82f6;
                outline: none;
                background-color: white;
                color: #1f2937;
            }
            QLineEdit:disabled, QComboBox:disabled, QTextEdit:disabled {
                background-color: #f3f4f6;
                color: #9ca3af;
            }
            QTableWidget {
                background-color: white;
                color: #1f2937;
                gridline-color: #e5e7eb;
                border: 1px solid #e5e7eb;
                border-radius: 6px;
            }
            QTableWidget::item {
                padding: 8px;
                color: #1f2937;
                border-bottom: 1px solid #e5e7eb;
            }
            QTableWidget::item:selected {
                background-color: #dbeafe;
                color: #1f2937;
            }
            QHeaderView::section {
                background-color: #f3f4f6;
                color: #1f2937;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #d1d5db;
                font-weight: 500;
            }
            QTableWidget QTableCornerButton::section {
                background-color: #f3f4f6;
                border: none;
                border-bottom: 2px solid #d1d5db;
                border-right: 1px solid #d1d5db;
            }
            QTableWidget QScrollBar:vertical {
                border: none;
                background: #f3f4f6;
                width: 10px;
                margin: 0px;
            }
            QTableWidget QScrollBar::handle:vertical {
                background: #9ca3af;
                min-height: 20px;
                border-radius: 5px;
            }
            QTableWidget QScrollBar::add-line:vertical, 
            QTableWidget QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QDialog {
                background-color: white;
            }
            QDialog QLabel {
                color: #4b5563;
                font-weight: 500;
            }
            #btn_eliminar {
                background-color: #ef4444;
                color: white;
            }
            #btn_eliminar:hover {
                background-color: #dc2626;
            }
            #btn_eliminar:disabled {
                background-color: #fca5a5;
            }
        """)
        
        # Aplicar estilos específicos a los botones de eliminación
        for tab in [self.cliente_tab, self.producto_tab, self.factura_tab]:
            if tab:
                for btn in tab.findChildren(QPushButton):
                    if btn.text() in ["Eliminar"]:
                        btn.setObjectName("btn_eliminar")

    def cargar_clientes(self):
        """Cargar la lista de clientes en la tabla"""
        try:
            clientes = self.cliente_service.get_clientes()
            self.tabla_clientes.setRowCount(0)
            
            for row, cliente in enumerate(clientes):
                self.tabla_clientes.insertRow(row)
                self.tabla_clientes.setItem(row, 0, QTableWidgetItem(str(cliente.id)))
                self.tabla_clientes.setItem(row, 1, QTableWidgetItem(f"{cliente.nombre} {cliente.apellido}"))
                self.tabla_clientes.setItem(row, 2, QTableWidgetItem(cliente.email or ""))
                self.tabla_clientes.setItem(row, 3, QTableWidgetItem(cliente.telefono or ""))
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar clientes: {str(e)}")

    def cargar_productos(self):
        """Cargar la lista de productos en la tabla"""
        try:
            productos = self.producto_service.get_productos()
            self.tabla_productos.setRowCount(0)
            
            for row, producto in enumerate(productos):
                self.tabla_productos.insertRow(row)
                self.tabla_productos.setItem(row, 0, QTableWidgetItem(str(producto.id)))
                self.tabla_productos.setItem(row, 1, QTableWidgetItem(producto.nombre))
                self.tabla_productos.setItem(row, 2, QTableWidgetItem(producto.codigo))
                self.tabla_productos.setItem(row, 3, QTableWidgetItem(str(producto.precio)))
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar productos: {str(e)}")

    def cargar_facturas(self):
        """Cargar la lista de facturas en la tabla"""
        try:
            facturas = self.factura_service.get_facturas()
            self.tabla_facturas.setRowCount(0)
            
            for row, factura in enumerate(facturas):
                self.tabla_facturas.insertRow(row)
                # Crear el ítem para la columna de ID
                id_item = QTableWidgetItem(str(factura.id))
                id_item.setData(Qt.ItemDataRole.UserRole, factura.id)  # Establecer el ID como UserRole
                self.tabla_facturas.setItem(row, 0, id_item)
                
                # Resto de las columnas
                self.tabla_facturas.setItem(row, 1, QTableWidgetItem(str(factura.numero_factura)))
                self.tabla_facturas.setItem(row, 2, QTableWidgetItem(factura.fecha_emision.strftime("%Y-%m-%d")))
                self.tabla_facturas.setItem(row, 3, QTableWidgetItem(str(factura.total)))
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar facturas: {str(e)}")

    def agregar_cliente(self):
        """Mostrar diálogo para agregar un nuevo cliente"""
        dialog = ClienteDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                # Obtener los datos del diálogo
                cliente_data = dialog.get_data()

                # Crear el diccionario con los datos del cliente
                from datetime import datetime
                cliente_dict = {
                    'nombre': cliente_data['nombre'],
                    'apellido': cliente_data['apellido'],
                    'dni': cliente_data['dni'],
                    'telefono': cliente_data['telefono'],
                    'email': cliente_data['email'],
                    'direccion': cliente_data['direccion'],
                    'fecha_creacion': datetime.now()
                }

                # Llamar al servicio con el diccionario
                self.cliente_service.create_cliente(cliente_dict)
                self.cargar_clientes()
                QMessageBox.information(self, "Éxito", "Cliente agregado correctamente")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al agregar cliente: {str(e)}")

    def agregar_producto(self):
        """Mostrar diálogo para agregar un nuevo producto"""
        dialog = ProductoDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                # Obtener los datos del diálogo
                producto_data = dialog.get_data()

                # Crear el diccionario con los datos del producto
                producto_dict = {
                    'nombre': producto_data['nombre'],
                    'codigo': producto_data['codigo'],
                    'precio': producto_data['precio'],
                    'descripcion': producto_data['descripcion']
                }

                # Llamar al servicio con el diccionario
                self.producto_service.create_producto(producto_dict)
                self.cargar_productos()
                QMessageBox.information(self, "Éxito", "Producto agregado correctamente")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al agregar producto: {str(e)}")

    def agregar_factura(self):
        """Mostrar diálogo para agregar una nueva factura"""
        dialog = FacturaDialog(self, self.db)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                factura_data = dialog.get_data()
                self.factura_service.create_factura(factura_data)
                self.cargar_facturas()
                QMessageBox.information(self, "Éxito", "Factura agregada correctamente")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al agregar factura: {str(e)}")

    def editar_factura(self):
        """Mostrar diálogo para editar una factura existente"""
        selected_items = self.tabla_facturas.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Error", "Seleccione una factura para editar")
            return

        # Obtener el ID de la factura seleccionada
        row = selected_items[0].row()
        factura_id = self.tabla_facturas.item(row, 0).data(Qt.ItemDataRole.UserRole)

        if not factura_id:
            QMessageBox.warning(self, "Error", "No se pudo obtener el ID de la factura")
            return

        factura = self.factura_service.get_factura(factura_id)

        if not factura:
            QMessageBox.warning(self, "Error", "No se pudo cargar la factura seleccionada")
            return

        dialog = FacturaDialog(self, self.db, factura)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                factura_data = dialog.get_data()
                self.factura_service.update_factura(factura_id, factura_data)
                self.cargar_facturas()
                QMessageBox.information(self, "Éxito", "Factura actualizada correctamente")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al actualizar factura: {str(e)}")

    def editar_producto(self):
        """Mostrar diálogo para editar un producto existente"""
        selected = self.tabla_productos.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Advertencia", "Por favor seleccione un producto")
            return

        producto_id = int(self.tabla_productos.item(selected[0].row(), 0).text())
        producto = self.producto_service.get_producto(producto_id)

        if not producto:
            QMessageBox.warning(self, "Error", "Producto no encontrado")
            return

        dialog = ProductoDialog(self, producto)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                # Obtener los datos del diálogo
                producto_data = dialog.get_data()

                # Crear el diccionario con los datos del producto
                update_data = {
                    'nombre': producto_data['nombre'],
                    'codigo': producto_data['codigo'],
                    'precio': producto_data['precio'],
                    'descripcion': producto_data['descripcion']
                }

                # Llamar al servicio con el diccionario
                self.producto_service.update_producto(producto_id, update_data)
                self.cargar_productos()
                QMessageBox.information(self, "Éxito", "Producto actualizado correctamente")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al actualizar producto: {str(e)}")

    def editar_factura(self):
        """Mostrar diálogo para editar una factura existente"""
        fila = self.tabla_facturas.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Error", "Seleccione una factura para editar")
            return

        factura_id = self.tabla_facturas.item(fila, 0).data(Qt.ItemDataRole.UserRole)
        factura = self.factura_service.get_factura(factura_id)
        
        if not factura:
            QMessageBox.warning(self, "Error", "No se pudo cargar la factura seleccionada")
            return

        dialog = FacturaDialog(self, self.db, factura)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                factura_data = dialog.get_data()
                self.factura_service.update_factura(factura_id, factura_data)
                self.cargar_facturas()
                QMessageBox.information(self, "Éxito", "Factura actualizada correctamente")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al actualizar factura: {str(e)}")

    def editar_cliente(self):
        """Mostrar diálogo para editar un cliente existente"""
        selected = self.tabla_clientes.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Advertencia", "Por favor seleccione un cliente")
            return

        cliente_id = int(self.tabla_clientes.item(selected[0].row(), 0).text())
        cliente = self.cliente_service.get_cliente(cliente_id)

        if not cliente:
            QMessageBox.warning(self, "Error", "Cliente no encontrado")
            return

        dialog = ClienteDialog(self, cliente)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                # Obtener los datos del diálogo
                cliente_data = dialog.get_data()

                # Crear el diccionario con los datos del cliente
                update_data = {
                    'nombre': cliente_data['nombre'],
                    'apellido': cliente_data['apellido'],
                    'dni': cliente_data['dni'],
                    'telefono': cliente_data['telefono'],
                    'email': cliente_data['email'],
                    'direccion': cliente_data['direccion']
                }

                # Llamar al servicio con el diccionario
                self.cliente_service.update_cliente(cliente_id, update_data)
                self.cargar_clientes()
                QMessageBox.information(self, "Éxito", "Cliente actualizado correctamente")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al actualizar cliente: {str(e)}")

    def eliminar_cliente(self):
        """Eliminar el cliente seleccionado"""
        selected = self.tabla_clientes.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Advertencia", "Por favor seleccione un cliente")
            return
            
        cliente_id = int(self.tabla_clientes.item(selected[0].row(), 0).text())
        
        reply = QMessageBox.question(
            self, 'Confirmar',
            '¿Está seguro de eliminar este cliente?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.cliente_service.delete_cliente(cliente_id)
                self.cargar_clientes()
                QMessageBox.information(self, "Éxito", "Cliente eliminado correctamente")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al eliminar cliente: {str(e)}")

    def eliminar_producto(self):
        """Eliminar el producto seleccionado"""
        selected = self.tabla_productos.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Advertencia", "Por favor seleccione un producto")
            return
            
        producto_id = int(self.tabla_productos.item(selected[0].row(), 0).text())
        
        reply = QMessageBox.question(
            self, 'Confirmar',
            '¿Está seguro de eliminar este producto?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.producto_service.delete_producto(producto_id)
                self.cargar_productos()
                QMessageBox.information(self, "Éxito", "Producto eliminado correctamente")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al eliminar producto: {str(e)}")

    def eliminar_factura(self):
        """Eliminar la factura seleccionada"""
        selected = self.tabla_facturas.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Advertencia", "Por favor seleccione una factura")
            return
            
        factura_id = int(self.tabla_facturas.item(selected[0].row(), 0).text())
        
        reply = QMessageBox.question(
            self, 'Confirmar',
            '¿Está seguro de eliminar esta factura?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.factura_service.delete_factura(factura_id)
                self.cargar_facturas()
                QMessageBox.information(self, "Éxito", "Factura eliminada correctamente")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al eliminar factura: {str(e)}")

    def buscar_cliente(self, texto):
        """Buscar clientes por nombre o DNI"""
        try:
            clientes = self.cliente_service.buscar_clientes(texto)
            self.tabla_clientes.setRowCount(0)
            
            for row, cliente in enumerate(clientes):
                self.tabla_clientes.insertRow(row)
                self.tabla_clientes.setItem(row, 0, QTableWidgetItem(str(cliente.id)))
                self.tabla_clientes.setItem(row, 1, QTableWidgetItem(f"{cliente.nombre} {cliente.apellido}"))
                self.tabla_clientes.setItem(row, 2, QTableWidgetItem(cliente.email or ""))
                self.tabla_clientes.setItem(row, 3, QTableWidgetItem(cliente.telefono or ""))
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al buscar clientes: {str(e)}")

    def buscar_producto(self, texto):
        """Buscar productos por nombre o código"""
        try:
            productos = self.producto_service.buscar_productos(texto)
            self.tabla_productos.setRowCount(0)
            
            for row, producto in enumerate(productos):
                self.tabla_productos.insertRow(row)
                self.tabla_productos.setItem(row, 0, QTableWidgetItem(str(producto.id)))
                self.tabla_productos.setItem(row, 1, QTableWidgetItem(producto.nombre))
                self.tabla_productos.setItem(row, 2, QTableWidgetItem(producto.codigo))
                self.tabla_productos.setItem(row, 3, QTableWidgetItem(str(producto.precio)))
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al buscar productos: {str(e)}")

    def buscar_factura(self, texto):
        """Buscar facturas por número o fecha"""
        try:
            facturas = self.factura_service.buscar_facturas(texto)
            self.tabla_facturas.setRowCount(0)
            
            for row, factura in enumerate(facturas):
                self.tabla_facturas.insertRow(row)
                self.tabla_facturas.setItem(row, 0, QTableWidgetItem(str(factura.id)))
                self.tabla_facturas.setItem(row, 1, QTableWidgetItem(str(factura.numero_factura)))
                self.tabla_facturas.setItem(row, 2, QTableWidgetItem(factura.fecha_emision.strftime("%Y-%m-%d")))
                self.tabla_facturas.setItem(row, 3, QTableWidgetItem(str(factura.total)))
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al buscar facturas: {str(e)}")

    def closeEvent(self, event):
        """Cerrar la conexión a la base de datos al cerrar la aplicación"""
        self.db.close()
        event.accept()


class ClienteDialog(QDialog):
    def __init__(self, parent=None, cliente=None):
        super().__init__(parent)
        self.cliente = cliente
        self.setWindowTitle("Nuevo Cliente" if not cliente else "Editar Cliente")
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()
        
        self.nombre_input = QLineEdit()
        self.apellido_input = QLineEdit()
        self.dni_input = QLineEdit()
        self.telefono_input = QLineEdit()
        self.email_input = QLineEdit()
        self.direccion_input = QLineEdit()
        
        if self.cliente:
            self.nombre_input.setText(self.cliente.nombre)
            self.apellido_input.setText(self.cliente.apellido)
            self.dni_input.setText(self.cliente.dni)
            self.telefono_input.setText(self.cliente.telefono or "")
            self.email_input.setText(self.cliente.email or "")
            self.direccion_input.setText(self.cliente.direccion or "")
        
        form.addRow("Nombre:", self.nombre_input)
        form.addRow("Apellido:", self.apellido_input)
        form.addRow("DNI:", self.dni_input)
        form.addRow("Teléfono:", self.telefono_input)
        form.addRow("Email:", self.email_input)
        form.addRow("Dirección:", self.direccion_input)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        layout.addLayout(form)
        layout.addWidget(buttons)
    
    def get_data(self):
        """Obtener los datos del formulario"""
        return {
            'nombre': self.nombre_input.text().strip(),
            'apellido': self.apellido_input.text().strip(),
            'dni': self.dni_input.text().strip(),
            'telefono': self.telefono_input.text().strip() or None,
            'email': self.email_input.text().strip() or None,
            'direccion': self.direccion_input.text().strip() or None
        }


class ProductoDialog(QDialog):
    def __init__(self, parent=None, producto=None):
        super().__init__(parent)
        self.producto = producto
        self.setWindowTitle("Nuevo Producto" if not producto else "Editar Producto")
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()
        
        self.nombre_input = QLineEdit()
        self.codigo_input = QLineEdit()
        self.precio_input = QLineEdit()
        self.descripcion_input = QLineEdit()
        
        if self.producto:
            self.nombre_input.setText(self.producto.nombre)
            self.codigo_input.setText(self.producto.codigo)
            self.precio_input.setText(str(self.producto.precio))
            self.descripcion_input.setText(self.producto.descripcion or "")
        
        form.addRow("Nombre:", self.nombre_input)
        form.addRow("Código:", self.codigo_input)
        form.addRow("Precio:", self.precio_input)
        form.addRow("Descripción:", self.descripcion_input)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        layout.addLayout(form)
        layout.addWidget(buttons)
    
    def get_data(self):
        """Obtener los datos del formulario"""
        return {
            'nombre': self.nombre_input.text().strip(),
            'codigo': self.codigo_input.text().strip(),
            'precio': float(self.precio_input.text().strip()),
            'descripcion': self.descripcion_input.text().strip() or None
        }