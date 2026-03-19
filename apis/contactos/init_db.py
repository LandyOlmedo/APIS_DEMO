import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "agendadb.sqlite3")

def init_database():
    """Inicializa la base de datos y crea la tabla contactos"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contactos (
            id_contacto INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)
    
    cursor.execute("SELECT COUNT(*) FROM contactos")
    count = cursor.fetchone()[0]
    
    if count == 0:
        print("100 registros")
        nombres = [
            "Juan", "María", "Pedro", "Ana", "Luis", "Carmen", "José", "Laura", 
            "Carlos", "Elena", "Miguel", "Sara", "Antonio", "Lucía", "Francisco",
            "Isabel", "Manuel", "Patricia", "David", "Marta"
        ]
        
        apellidos = [
            "García", "Rodríguez", "González", "Fernández", "López", "Martínez",
            "Sánchez", "Pérez", "Martín", "Gómez"
        ]
        
        contactos = []
        for i in range(1, 101):
            nombre = f"{nombres[i % len(nombres)]} {apellidos[i % len(apellidos)]}"
            telefono = f"{5550000 + i:010d}"
            email = f"contacto{i}@example.com"
            contactos.append((nombre, telefono, email))
        
        cursor.executemany(
            "INSERT INTO contactos (nombre, telefono, email) VALUES (?, ?, ?)",
            contactos
        )
        
        conn.commit()
        print(f"✓ {len(contactos)} registros insertados correctamente")
    else:
        print(f"La base de datos ya contiene {count} registros")
    
    conn.close()
    print(f"✓ Base de datos inicializada en: {DB_PATH}")

if __name__ == "__main__":
    init_database()
