from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
                             QDateEdit, QComboBox, QDialogButtonBox, QMessageBox, 
                             QTabWidget, QWidget, QTableWidget, QTableWidgetItem, 
                             QPushButton, QHeaderView, QSpinBox, QDoubleSpinBox, 
                             QLabel, QHBoxLayout)
from PyQt6.QtCore import Qt, QDate
from datetime import datetime
from app.models.cliente import Cliente
from app.models.producto import Producto
from app.schemas.factura import FacturaCreate, DetalleFacturaCreate
from app.services.cliente_service import ClienteService
from app.services.producto_service import ProductoService

class FacturaDialog(QDialog):
    def __init__(self, parent=None, db=None, factura=None):
        super().__init__(parent)
        self.db = db
        self.factura = factura
        self.clientes = []
        self.productos = []
        # Initialize detalles with existing factura's detalles if editing, otherwise empty list
        self.detalles = [detalle for detalle in factura.detalles] if factura and hasattr(factura, 'detalles') else []
        self.setWindowTitle("Nueva Factura" if not factura else "Editar Factura")
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Aplicar estilos
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                color: black;
            }
            QLineEdit, QComboBox, QDateEdit, QSpinBox, QDoubleSpinBox {
                background-color: white;
                color: black;
                border: 1px solid #d0d0d0;
                padding: 5px;
                border-radius: 3px;
            }
            QTableWidget {
                background-color: white;
                color: black;
                gridline-color: #d0d0d0;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 5px;
                border: 1px solid #d0d0d0;
            }
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #d0d0d0;
                padding: 5px 10px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        
        # Pestañas
        tabs = QTabWidget()
        
        # Pestaña de datos generales
        datos_widget = QWidget()
        self.setup_datos_tab(datos_widget)
        tabs.addTab(datos_widget, "Datos Generales")
        
        # Pestaña de detalles
        detalles_widget = QWidget()
        self.setup_detalles_tab(detalles_widget)
        tabs.addTab(detalles_widget, "Detalles")
        
        layout.addWidget(tabs)
        
        # Botones
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        # Cargar datos iniciales
        self.cargar_clientes()
        self.cargar_productos()  # Asegurarse de cargar los productos
        
        if self.factura:
            self.cargar_datos_factura()
        
    def setup_datos_tab(self, parent):
        layout = QFormLayout()
        
        # Número de factura (se generará automáticamente)
        self.numero_input = QLineEdit()
        self.numero_input.setReadOnly(True)
        self.numero_input.setText("Generado automáticamente")
        
        # Fecha actual
        self.fecha_input = QDateEdit()
        self.fecha_input.setCalendarPopup(True)
        self.fecha_input.setDate(QDate.currentDate())
        
        # Cliente
        self.cliente_combo = QComboBox()
        
        # Estado
        self.estado_combo = QComboBox()
        self.estado_combo.addItems(["PENDIENTE", "PAGADA", "ANULADA"])
        
        # Impuesto
        self.impuesto_input = QDoubleSpinBox()
        self.impuesto_input.setRange(0, 100)
        self.impuesto_input.setValue(16.0)  # 16% por defecto
        self.impuesto_input.setSuffix("%")
        
        # Totales
        self.subtotal_label = QLabel("0.00")
        self.impuesto_label = QLabel("0.00")
        self.total_label = QLabel("0.00")
        
        # Agregar widgets al formulario
        layout.addRow("Número:", self.numero_input)
        layout.addRow("Fecha:", self.fecha_input)
        layout.addRow("Cliente:", self.cliente_combo)
        layout.addRow("Estado:", self.estado_combo)
        layout.addRow("Impuesto (%%):", self.impuesto_input)
        layout.addRow("Subtotal:", self.subtotal_label)
        layout.addRow("Impuesto:", self.impuesto_label)
        layout.addRow("Total:", self.total_label)
        
        parent.setLayout(layout)
        
    def setup_detalles_tab(self, parent):
        layout = QVBoxLayout()
        
        # Formulario para agregar detalles
        form_layout = QHBoxLayout()
        
        # Producto
        self.producto_combo = QComboBox()
        
        # Cantidad
        self.cantidad_input = QSpinBox()
        self.cantidad_input.setMinimum(1)
        self.cantidad_input.setValue(1)
        
        # Precio unitario
        self.precio_input = QDoubleSpinBox()
        self.precio_input.setMinimum(0.01)
        self.precio_input.setMaximum(999999.99)
        
        # Botón para agregar
        agregar_button = QPushButton("Agregar")
        agregar_button.clicked.connect(self.agregar_detalle)
        
        # Agregar widgets al formulario
        form_layout.addWidget(QLabel("Producto:"))
        form_layout.addWidget(self.producto_combo, 2)
        form_layout.addWidget(QLabel("Cantidad:"))
        form_layout.addWidget(self.cantidad_input)
        form_layout.addWidget(QLabel("Precio:"))
        form_layout.addWidget(self.precio_input)
        form_layout.addWidget(agregar_button)
        
        # Tabla de detalles
        self.detalles_table = QTableWidget()
        self.detalles_table.setColumnCount(5)
        self.detalles_table.setHorizontalHeaderLabels(["Producto", "Cantidad", "Precio Unit.", "Subtotal", ""])
        
        # Configurar el ancho de las columnas
        header = self.detalles_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Producto se expande
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Cantidad
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Precio Unit.
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Subtotal
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Columna de botón
        
        # Configurar el alto de las filas
        self.detalles_table.verticalHeader().setDefaultSectionSize(35)  # Aumentar el alto de las filas
        self.detalles_table.verticalHeader().setVisible(False)  # Ocultar los números de fila
        
        # Mejorar la apariencia de la tabla
        self.detalles_table.setAlternatingRowColors(True)  # Filas alternas de colores
        self.detalles_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.detalles_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        layout.addLayout(form_layout)
        layout.addWidget(self.detalles_table)
        
        parent.setLayout(layout)
        
    def cargar_clientes(self):
        """Cargar la lista de clientes en el combo box"""
        cliente_service = ClienteService(self.db)
        self.clientes = cliente_service.get_clientes()
        
        self.cliente_combo.clear()
        for cliente in self.clientes:
            self.cliente_combo.addItem(f"{cliente.nombre} {cliente.apellido}", cliente.id)
            
    def cargar_productos(self):
        """Cargar la lista de productos en el combo box"""
        producto_service = ProductoService(self.db)
        self.productos = producto_service.get_productos()
        
        self.producto_combo.clear()
        for producto in self.productos:
            if producto.stock > 0:  # Solo mostrar productos con stock disponible
                self.producto_combo.addItem(
                    f"{producto.nombre} - ${producto.precio:.2f} (Stock: {producto.stock})",
                    producto.id
                )
                
    def cargar_datos_factura(self):
        """Cargar los datos de la factura en el formulario"""
        if not self.factura:
            return

        self.numero_input.setText(str(self.factura.numero_factura))
        self.fecha_input.setDate(QDate.fromString(self.factura.fecha_emision.strftime("%Y-%m-%d"), "yyyy-MM-dd"))

        # Buscar el índice del cliente en el combo
        index = self.cliente_combo.findData(self.factura.cliente_id)
        if index >= 0:
            self.cliente_combo.setCurrentIndex(index)

        self.estado_combo.setCurrentText(self.factura.estado)
        self.impuesto_input.setValue(self.factura.impuesto)

        # Cargar detalles con DetalleFacturaCreate
        for detalle in self.factura.detalles:
            self.detalles.append(DetalleFacturaCreate(
                producto_id=detalle.producto_id,
                cantidad=detalle.cantidad,
                precio_unitario=detalle.precio_unitario
            ))

        self.actualizar_tabla_detalles()
        self.actualizar_totales()

    def agregar_detalle(self):
        producto_index = self.producto_combo.currentIndex()
        if producto_index < 0:
            QMessageBox.warning(self, "Error", "Seleccione un producto")
            return
            
        producto_id = self.producto_combo.itemData(producto_index)
        producto_text = self.producto_combo.currentText().split(" - ")[0]  # Obtener solo el nombre
        cantidad = self.cantidad_input.value()
        precio = self.precio_input.value()
        
        # Verificar si el producto ya está en los detalles
        for i, detalle in enumerate(self.detalles):
            if detalle.producto_id == producto_id:
                # Preguntar si desea actualizar la cantidad
                reply = QMessageBox.question(
                    self,
                    "Producto existente",
                    f"El producto ya está en la lista. ¿Desea actualizar la cantidad?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                
                if reply == QMessageBox.StandardButton.Yes:
                    # Actualizar cantidad y subtotal
                    self.detalles[i].cantidad = cantidad
                    self.detalles[i].precio_unitario = precio
                    self.actualizar_tabla_detalles()
                    self.actualizar_totales()
                return
                
        # Agregar nuevo detalle
        detalle = DetalleFacturaCreate(
            producto_id=producto_id,
            cantidad=cantidad,
            precio_unitario=precio
        )
        self.detalles.append(detalle)
        
        # Actualizar la tabla y totales
        self.actualizar_tabla_detalles()
        self.actualizar_totales()
        
        # Resetear controles
        self.producto_combo.setCurrentIndex(-1)
        self.cantidad_input.setValue(1)
        
    def actualizar_tabla_detalles(self):
        self.detalles_table.setRowCount(0)
        
        for i, detalle in enumerate(self.detalles):
            producto = next((p for p in self.productos if p.id == detalle.producto_id), None)
            if not producto:
                continue
                
            row = self.detalles_table.rowCount()
            self.detalles_table.insertRow(row)
            
            # Producto
            self.detalles_table.setItem(row, 0, QTableWidgetItem(producto.nombre))
            
            # Cantidad
            self.detalles_table.setItem(row, 1, QTableWidgetItem(str(detalle.cantidad)))
            
            # Precio unitario
            self.detalles_table.setItem(row, 2, QTableWidgetItem(f"${detalle.precio_unitario:.2f}"))
            
            # Subtotal
            subtotal = detalle.cantidad * detalle.precio_unitario
            self.detalles_table.setItem(row, 3, QTableWidgetItem(f"${subtotal:.2f}"))
            
            # Botón para eliminar
            eliminar_button = QPushButton("Eliminar")
            eliminar_button.setProperty("row", i)
            eliminar_button.clicked.connect(self.eliminar_detalle)
            self.detalles_table.setCellWidget(row, 4, eliminar_button)
            
    def eliminar_detalle(self):
        sender = self.sender()
        if sender:
            row = sender.property("row")
            if 0 <= row < len(self.detalles):
                self.detalles.pop(row)
                self.actualizar_tabla_detalles()
                self.actualizar_totales()
                
    def actualizar_totales(self):
        # Calcular subtotal de la tabla de detalles
        subtotal = sum(detalle.cantidad * detalle.precio_unitario for detalle in self.detalles)
        
        # Actualizar etiquetas
        self.subtotal_label.setText(f"${subtotal:.2f}")
        
        # Calcular impuesto y total
        impuesto_porcentaje = self.impuesto_input.value()
        impuesto = subtotal * (impuesto_porcentaje / 100)
        total = subtotal + impuesto
        
        self.impuesto_label.setText(f"${impuesto:.2f}")
        self.total_label.setText(f"${total:.2f}")
        
    def validar_datos(self):
        """Validar los datos del formulario antes de aceptar"""
        if self.cliente_combo.currentIndex() < 0:
            QMessageBox.warning(self, "Error", "Debe seleccionar un cliente")
            return
            
        self.accept()

    def get_data(self):
        """Obtener los datos del formulario"""
        # Calcular subtotal, impuesto y total
        subtotal = sum(detalle.cantidad * detalle.precio_unitario for detalle in self.detalles)
        impuesto = subtotal * (self.impuesto_input.value() / 100)
        total = subtotal + impuesto

        # Convertir los detalles a diccionarios
        detalles_dict = [
            {
                'producto_id': detalle.producto_id,
                'cantidad': detalle.cantidad,
                'precio_unitario': float(detalle.precio_unitario)
            }
            for detalle in self.detalles
        ]

        return {
            'cliente_id': self.cliente_combo.currentData(),
            'fecha_emision': self.fecha_input.dateTime().toPyDateTime(),
            'estado': self.estado_combo.currentText(),
            'impuesto': float(self.impuesto_input.value()),
            'subtotal': float(subtotal),
            'total': float(total),
            'detalles': detalles_dict
        }