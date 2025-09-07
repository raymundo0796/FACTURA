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
        self.root.geometry("1000x600")
        self.root.configure(bg="#f5f6fa")

        self.items_factura = []

        # Estilo
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=("Arial", 11), rowheight=28)
        style.configure("TButton", font=("Arial", 11), padding=6)
        style.configure("TLabel", font=("Arial", 12), background="#f5f6fa")

        # Frame izquierdo (cliente y productos)
        frame_left = tk.Frame(self.root, bg="#f5f6fa", padx=15, pady=15)
        frame_left.pack(side="left", fill="y")

        ttk.Label(frame_left, text="👤 Cliente", font=("Arial", 14, "bold")).pack(pady=10)

        ttk.Label(frame_left, text="Nombre:").pack()
        self.entry_cliente = ttk.Entry(frame_left, width=30)
        self.entry_cliente.pack(pady=5)

        ttk.Label(frame_left, text="DNI:").pack()
        self.entry_dni = ttk.Entry(frame_left, width=30)
        self.entry_dni.pack(pady=5)

        ttk.Button(frame_left, text="➕ Registrar Cliente", command=self.registrar_cliente).pack(pady=10)

        # Productos
        ttk.Label(frame_left, text="📦 Productos Disponibles", font=("Arial", 14, "bold")).pack(pady=10)

        self.lista_productos = ttk.Combobox(frame_left, state="readonly", width=35, font=("Arial", 11))
        self.lista_productos.pack(pady=5)

        self.actualizar_productos()

        ttk.Label(frame_left, text="Cantidad:").pack(pady=5)
        self.cantidad_spin = tk.Spinbox(frame_left, from_=1, to=100, font=("Arial", 11), width=5)
        self.cantidad_spin.pack(pady=5)

        ttk.Button(frame_left, text="➕ Agregar a Factura", command=self.agregar_a_factura).pack(pady=10)

        # Frame derecho (factura)
        frame_right = tk.Frame(self.root, bg="#f5f6fa", padx=15, pady=15)
        frame_right.pack(side="right", fill="both", expand=True)

        ttk.Label(frame_right, text="🧾 Factura", font=("Arial", 14, "bold")).pack(pady=10)

        self.tabla_factura = ttk.Treeview(frame_right, columns=("Producto", "Precio", "Cantidad", "Subtotal"), show="headings", height=15)
        self.tabla_factura.pack(fill="both", expand=True)

        self.tabla_factura.heading("Producto", text="Producto")
        self.tabla_factura.heading("Precio", text="Precio")
        self.tabla_factura.heading("Cantidad", text="Cantidad")
        self.tabla_factura.heading("Subtotal", text="Subtotal")

        self.label_total = ttk.Label(frame_right, text="💲 Total: $0.00", font=("Arial", 13, "bold"))
        self.label_total.pack(pady=10)

        # Botones
        btn_frame = tk.Frame(frame_right, bg="#f5f6fa")
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="❌ Eliminar", command=self.eliminar_item).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="💾 Guardar Factura", command=self.guardar_factura).grid(row=0, column=1, padx=5)

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
# MAIN
# ==========================
if __name__ == "__main__":
    inicializar_db()
    root = tk.Tk()
    app = FacturacionApp(root)
    root.mainloop()
