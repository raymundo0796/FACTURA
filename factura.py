import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import datetime

# ==========================
# BASE DE DATOS
# ==========================
def inicializar_db():
    conn = sqlite3.connect("facturacion.db")
    cursor = conn.cursor()

    # Tabla productos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL
    )
    """)
# Tabla Clientes
    # Tabla clientes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        dni TEXT UNIQUE NOT NULL
    )
    """)

    # Tabla facturas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS facturas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        fecha TEXT,
        total REAL,
        FOREIGN KEY(cliente_id) REFERENCES clientes(id)
    )
    """)

    # Tabla detalle factura
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS detalle_factura (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        factura_id INTEGER,
        producto_id INTEGER,
        cantidad INTEGER,
        subtotal REAL,
        FOREIGN KEY(factura_id) REFERENCES facturas(id),
        FOREIGN KEY(producto_id) REFERENCES productos(id)
    )
    """)

    conn.commit()
    conn.close()


# ==========================
# CLASE PRINCIPAL
# ==========================
class FacturacionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🧾 Sistema de Facturación Profesional")
        self.root.geometry("1100x650")
        # Fondo principal: verde muy suave
        self.root.configure(bg="#eafaf1")

        self.items_factura = []

        # Estilo
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=("Segoe UI", 11), rowheight=32, borderwidth=0, relief="flat",
                        background="#eafaf1", fieldbackground="#eafaf1")
        style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"), background="#b2f7ef", foreground="#000", borderwidth=0)
        style.configure("TButton", font=("Segoe UI", 11), padding=8, background="#4f8cff", foreground="#000", borderwidth=0)
        style.map("TButton", background=[("active", "#43d19e")])
        style.configure("TLabel", font=("Segoe UI", 12), background="#eafaf1", foreground="#000")
        style.configure("TEntry", font=("Segoe UI", 11))
        style.configure("TCombobox", font=("Segoe UI", 11))
        style.configure("TSpinbox", font=("Segoe UI", 11))

        # Título principal
        titulo = tk.Label(self.root, text="🧾 Sistema de Facturación Profesional", font=("Segoe UI", 22, "bold"), bg="#eafaf1", fg="#000")
        titulo.pack(pady=(18, 0))

        # Frame principal
        main_frame = tk.Frame(self.root, bg="#eafaf1")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Frame izquierdo (cliente y productos)
        frame_left = tk.Frame(main_frame, bg="#b2f7ef", padx=20, pady=20, bd=0, relief="flat", highlightbackground="#43d19e", highlightthickness=2)
        frame_left.pack(side="left", fill="y", padx=(0, 18), pady=10)

        ttk.Label(frame_left, text="👤 Cliente", font=("Segoe UI", 15, "bold"), background="#b2f7ef", foreground="#000").pack(pady=(0, 12))

        ttk.Label(frame_left, text="Nombre:", background="#b2f7ef", foreground="#000").pack(anchor="w")
        self.entry_cliente = ttk.Entry(frame_left, width=28)
        self.entry_cliente.pack(pady=4)

        ttk.Label(frame_left, text="DNI:", background="#b2f7ef", foreground="#000").pack(anchor="w")
        self.entry_dni = ttk.Entry(frame_left, width=28)
        self.entry_dni.pack(pady=4)

        ttk.Button(frame_left, text="➕ Registrar Cliente", command=self.registrar_cliente).pack(pady=12, fill="x")

        ttk.Separator(frame_left, orient="horizontal").pack(fill="x", pady=12)

        ttk.Label(frame_left, text="📦 Productos Disponibles", font=("Segoe UI", 15, "bold"), background="#b2f7ef", foreground="#000").pack(pady=(0, 12))

        self.lista_productos = ttk.Combobox(frame_left, state="readonly", width=30, font=("Segoe UI", 11))
        self.lista_productos.pack(pady=4)

        self.actualizar_productos()

        ttk.Label(frame_left, text="Cantidad:", background="#b2f7ef", foreground="#000").pack(anchor="w", pady=(8, 0))
        self.cantidad_spin = tk.Spinbox(frame_left, from_=1, to=100, font=("Segoe UI", 11), width=6, relief="flat", bd=1)
        self.cantidad_spin.pack(pady=4)

        ttk.Button(frame_left, text="➕ Agregar a Factura", command=self.agregar_a_factura).pack(pady=12, fill="x")

        # Frame derecho (factura)
        frame_right = tk.Frame(main_frame, bg="#ffffff", padx=20, pady=20, bd=0, relief="flat", highlightbackground="#43d19e", highlightthickness=2)
        frame_right.pack(side="right", fill="both", expand=True, pady=10)

        ttk.Label(frame_right, text="🧾 Factura", font=("Segoe UI", 15, "bold"), background="#ffffff", foreground="#000").pack(pady=(0, 12))

        self.tabla_factura = ttk.Treeview(frame_right, columns=("Producto", "Precio", "Cantidad", "Subtotal"), show="headings", height=15)
        self.tabla_factura.pack(fill="both", expand=True, pady=8)

        self.tabla_factura.heading("Producto", text="Producto")
        self.tabla_factura.heading("Precio", text="Precio")
        self.tabla_factura.heading("Cantidad", text="Cantidad")
        self.tabla_factura.heading("Subtotal", text="Subtotal")

        self.label_total = ttk.Label(frame_right, text="💲 Total: $0.00", font=("Segoe UI", 14, "bold"), background="#ffffff", foreground="#000")
        self.label_total.pack(pady=10, anchor="e")

        # Botones
        btn_frame = tk.Frame(frame_right, bg="#ffffff")
        btn_frame.pack(pady=5, anchor="e")

        ttk.Button(btn_frame, text="❌ Eliminar", command=self.eliminar_item).grid(row=0, column=0, padx=6)
        ttk.Button(btn_frame, text="💾 Guardar Factura", command=self.guardar_factura).grid(row=0, column=1, padx=6)

    # ==========================
    # FUNCIONES
    # ==========================
    def actualizar_productos(self):
        conn = sqlite3.connect("facturacion.db")
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM productos")
        productos = [row[0] for row in cursor.fetchall()]
        conn.close()

        self.lista_productos["values"] = productos

    def registrar_cliente(self):
        nombre = self.entry_cliente.get()
        dni = self.entry_dni.get()

        if not nombre or not dni:
            messagebox.showwarning("Aviso", "⚠️ Debes ingresar nombre y DNI.")
            return

        conn = sqlite3.connect("facturacion.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO clientes (nombre, dni) VALUES (?, ?)", (nombre, dni))
            conn.commit()
            messagebox.showinfo("Éxito", "✅ Cliente registrado correctamente.")
        except sqlite3.IntegrityError:
            messagebox.showwarning("Aviso", "⚠️ El DNI ya está registrado.")
        conn.close()

    def agregar_a_factura(self):
        producto_nombre = self.lista_productos.get()
        if not producto_nombre:
            messagebox.showwarning("Aviso", "⚠️ Selecciona un producto.")
            return

        cantidad = int(self.cantidad_spin.get())

        conn = sqlite3.connect("facturacion.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, precio FROM productos WHERE nombre=?", (producto_nombre,))
        producto = cursor.fetchone()
        conn.close()

        if producto:
            producto_id, precio = producto
            subtotal = precio * cantidad
            self.items_factura.append((producto_id, producto_nombre, precio, cantidad, subtotal))
            self.tabla_factura.insert("", "end", values=(producto_nombre, f"${precio:.2f}", cantidad, f"${subtotal:.2f}"))
            self.actualizar_total()

    def actualizar_total(self):
        total = sum(item[4] for item in self.items_factura)
        self.label_total.config(text=f"💲 Total: ${total:.2f}")

    def eliminar_item(self):
        seleccionado = self.tabla_factura.selection()
        if not seleccionado:
            messagebox.showwarning("Aviso", "⚠️ Selecciona un producto en la factura.")
            return

        index = self.tabla_factura.index(seleccionado)
        self.tabla_factura.delete(seleccionado)
        self.items_factura.pop(index)
        self.actualizar_total()

    def guardar_factura(self):
        if not self.items_factura:
            messagebox.showwarning("Aviso", "⚠️ No hay productos en la factura.")
            return

        cliente_nombre = self.entry_cliente.get()
        dni = self.entry_dni.get()

        if not cliente_nombre or not dni:
            messagebox.showwarning("Aviso", "⚠️ Debes ingresar los datos del cliente.")
            return

        conn = sqlite3.connect("facturacion.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM clientes WHERE dni=?", (dni,))
        cliente = cursor.fetchone()

        if not cliente:
            messagebox.showwarning("Aviso", "⚠️ El cliente no está registrado.")
            conn.close()
            return

        cliente_id = cliente[0]
        total = sum(item[4] for item in self.items_factura)
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("INSERT INTO facturas (cliente_id, fecha, total) VALUES (?, ?, ?)", (cliente_id, fecha, total))
        factura_id = cursor.lastrowid

        for item in self.items_factura:
            producto_id, _, _, cantidad, subtotal = item
            cursor.execute("INSERT INTO detalle_factura (factura_id, producto_id, cantidad, subtotal) VALUES (?, ?, ?, ?)", (factura_id, producto_id, cantidad, subtotal))

        conn.commit()
        conn.close()

        # Guardar en archivo
        with open(f"factura_{factura_id}.txt", "w") as f:
            f.write("=== FACTURA ===\n")
            f.write(f"Cliente: {cliente_nombre}\nDNI: {dni}\nFecha: {fecha}\n\n")
            for item in self.items_factura:
                f.write(f"{item[1]} - ${item[2]:.2f} x {item[3]} = ${item[4]:.2f}\n")
            f.write(f"\nTOTAL: ${total:.2f}\n")

        self.items_factura.clear()
        for row in self.tabla_factura.get_children():
            self.tabla_factura.delete(row)
        self.actualizar_total()

        messagebox.showinfo("Éxito", f"✅ Factura guardada correctamente (ID: {factura_id}).")


# ==========================
# MENU
# ==========================
if __name__ == "__main__":
    inicializar_db()
    root = tk.Tk()
    app = FacturacionApp(root)
    root.mainloop()
