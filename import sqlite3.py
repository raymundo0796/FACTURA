import sqlite3

def insertar_productos():
    conn = sqlite3.connect("facturacion.db")
    cursor = conn.cursor()

    productos = [
        ("Laptop", 2500.00),
        ("Smartphone", 1200.00),
        ("Auriculares", 150.00),
        ("Mouse Gamer", 80.00),
        ("Teclado Mecánico", 200.00),
        ("Monitor 24 pulgadas", 900.00),
        ("Impresora Multifuncional", 650.00),
        ("Disco SSD 1TB", 350.00),
        ("Memoria RAM 16GB", 280.00),
        ("Cámara Web Full HD", 180.00)
    ]

    try:
        cursor.executemany("INSERT INTO productos (nombre, precio) VALUES (?, ?)", productos)
        conn.commit()
        print("✅ Productos iniciales insertados correctamente.")
    except Exception as e:
        print("⚠️ Error al insertar productos:", e)

    conn.close()


if __name__ == "__main__":
    insertar_productos()
