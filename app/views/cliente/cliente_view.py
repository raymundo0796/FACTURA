# app/views/cliente/cliente_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from app.views.base_view import BaseView
from app.services.cliente_service import ClienteService
from app.config.database import get_db


class ClienteView(BaseView):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.db = next(get_db())
        self.service = ClienteService(self.db)
        self.setup_ui()

    def setup_ui(self):
        # Frame principal
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Frame de formulario
        form_frame = ttk.LabelFrame(self.main_frame, text="Datos del Cliente", padding=10)
        form_frame.pack(fill=tk.X, pady=(0, 10))

        # Campos del formulario
        ttk.Label(form_frame, text="DNI:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.dni_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.dni_var, width=20).grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)

        ttk.Label(form_frame, text="Nombre:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.nombre_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.nombre_var, width=30).grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)

        # Botones
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(fill=tk.X, pady=10)

        ttk.Button(btn_frame, text="Guardar", command=self.guardar_cliente).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=self.limpiar_campos).pack(side=tk.LEFT, padx=5)

        # Tabla de clientes
        self.crear_tabla()

    def crear_tabla(self):
        # Crear el Treeview
        columns = ("dni", "nombre", "telefono", "email")
        self.tree = ttk.Treeview(self.main_frame, columns=columns, show="headings")

        # Configurar columnas
        self.tree.heading("dni", text="DNI")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("telefono", text="Teléfono")
        self.tree.heading("email", text="Email")

        # Ajustar ancho de columnas
        self.tree.column("dni", width=100)
        self.tree.column("nombre", width=200)
        self.tree.column("telefono", width=100)
        self.tree.column("email", width=200)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Cargar datos
        self.cargar_clientes()

    def cargar_clientes(self):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Cargar clientes
        clientes = self.service.get_clientes()
        for cliente in clientes:
            self.tree.insert("", tk.END, values=(
                cliente.dni,
                f"{cliente.nombre} {cliente.apellido}",
                cliente.telefono or "",
                cliente.email or ""
            ))

    def guardar_cliente(self):
        try:
            # Validar campos
            if not self.dni_var.get() or not self.nombre_var.get():
                messagebox.showwarning("Validación", "DNI y Nombre son campos obligatorios")
                return

            # Crear diccionario con los datos
            cliente_data = {
                "dni": self.dni_var.get(),
                "nombre": self.nombre_var.get().split()[0],
                "apellido": " ".join(self.nombre_var.get().split()[1:]) if " " in self.nombre_var.get() else "",
                "telefono": self.telefono_var.get() if hasattr(self, 'telefono_var') else None,
                "email": self.email_var.get() if hasattr(self, 'email_var') else None
            }

            # Guardar cliente
            self.service.create_cliente(cliente_data)
            messagebox.showinfo("Éxito", "Cliente guardado correctamente")
            self.limpiar_campos()
            self.cargar_clientes()

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el cliente: {str(e)}")

    def limpiar_campos(self):
        self.dni_var.set("")
        self.nombre_var.set("")
        if hasattr(self, 'telefono_var'):
            self.telefono_var.set("")
        if hasattr(self, 'email_var'):
            self.email_var.set("")