import sqlite3
import os
import csv

DB_PATH = os.path.join(os.path.dirname(__file__), "agendadb.sqlite3")
CSV_PATH = os.path.join(os.path.dirname(__file__), "data.csv")

def init_database():
    """Inicializa la base de datos y crea la tabla contactos"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contactos (
            id_contacto INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)
    
    cursor.execute("SELECT COUNT(*) FROM contactos")
    count = cursor.fetchone()[0]
    
    if count == 0:
        try:
            contactos = []
            with open(CSV_PATH, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    contactos.append((
                        int(row['id_contacto']),
                        row['nombre'],
                        row['telefono'],
                        row['email']
                    ))
            
            cursor.executemany(
                "INSERT INTO contactos (id_contacto, nombre, telefono, email) VALUES (?, ?, ?, ?)",
                contactos
            )
            
            conn.commit()
            print(f"✓ {len(contactos)} registros insertados correctamente desde CSV")
        except FileNotFoundError:
            print(f"⚠ Error: El archivo CSV no se encontró en {CSV_PATH}")
        except Exception as e:
            print(f"⚠ Error al cargar CSV: {e}")
    else:
        print(f"La base de datos ya contiene {count} registros")
    
    conn.close()
    print(f"✓ Base de datos inicializada en: {DB_PATH}")

if __name__ == "__main__":
    init_database()
