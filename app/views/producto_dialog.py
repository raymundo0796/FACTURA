from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QTextEdit, QDoubleSpinBox, QSpinBox,
    QPushButton, QMessageBox, QDialogButtonBox
)
from PyQt6.QtCore import Qt


class ProductoDialog(QDialog):
    def __init__(self, parent=None, producto=None):
        super().__init__(parent)
        self.setWindowTitle("Nuevo Producto" if not producto else "Editar Producto")
        self.setMinimumWidth(500)
        self.producto = producto

        self.setup_ui()

        if producto:
            self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Formulario
        form_layout = QFormLayout()

        self.codigo_input = QLineEdit()
        self.codigo_input.setMaxLength(50)

        self.nombre_input = QLineEdit()
        self.nombre_input.setMaxLength(200)

        self.descripcion_input = QTextEdit()
        self.descripcion_input.setMaximumHeight(100)

        self.precio_input = QDoubleSpinBox()
        self.precio_input.setRange(0, 999999.99)
        self.precio_input.setDecimals(2)
        self.precio_input.setPrefix("$")

        self.stock_input = QSpinBox()
        self.stock_input.setRange(0, 999999)

        form_layout.addRow("Código*:", self.codigo_input)
        form_layout.addRow("Nombre*:", self.nombre_input)
        form_layout.addRow("Descripción:", self.descripcion_input)
        form_layout.addRow("Precio*:", self.precio_input)
        form_layout.addRow("Stock*:", self.stock_input)

        # Botones
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addLayout(form_layout)
        layout.addWidget(button_box)

    def load_data(self):
        """Cargar datos del producto en el formulario"""
        if not self.producto:
            return

        self.codigo_input.setText(self.producto.codigo)
        self.nombre_input.setText(self.producto.nombre)
        self.descripcion_input.setPlainText(self.producto.descripcion or "")
        self.precio_input.setValue(self.producto.precio or 0)
        self.stock_input.setValue(self.producto.stock or 0)

    def get_data(self):
        """Obtener los datos del formulario"""
        return {
            "codigo": self.codigo_input.text().strip(),
            "nombre": self.nombre_input.text().strip(),
            "descripcion": self.descripcion_input.toPlainText().strip(),
            "precio": self.precio_input.value(),
            "stock": self.stock_input.value()
        }

    def validate(self):
        """Validar los datos del formulario"""
        data = self.get_data()

        if not data["codigo"]:
            QMessageBox.warning(self, "Error", "El código es obligatorio")
            return False

        if not data["nombre"]:
            QMessageBox.warning(self, "Error", "El nombre es obligatorio")
            return False

        if data["precio"] <= 0:
            QMessageBox.warning(self, "Error", "El precio debe ser mayor a cero")
            return False

        if data["stock"] < 0:
            QMessageBox.warning(self, "Error", "El stock no puede ser negativo")
            return False

        return True

    def accept(self):
        if self.validate():
            super().accept()
