# API REST de Agenda de Contactos - FastAPI

## Descripción

API REST completa desarrollada con FastAPI para gestionar una agenda de contactos. Incluye operaciones CRUD (Create, Read, Update, Delete) con paginación, búsqueda flexible y validación de parámetros.

## Características Implementadas

✅ **GET /** - Endpoint raíz con bienvenida  
✅ **GET /v1/contactos** - Listar contactos con paginación (limit, skip)  
✅ **GET /v1/contactos/{id_contacto}** - Obtener contacto por ID  
✅ **GET /v1/contacto** - Buscar contacto por nombre o ID  
✅ **POST /v1/contacto** - Crear nuevo contacto  
✅ **PUT /v1/contacto** - Modificar contacto por ID  
✅ **DELETE /v1/contacto** - Eliminar contacto por ID  

## Archivos Generados/Modificados

### 1. [init_db.py](init_db.py)
- **Modificado**: Carga datos del archivo CSV en lugar de generar datos ficticios
- Lee 100 contactos desde `data.csv`
- Inicializa la base de datos SQLite automáticamente

### 2. [main.py](main.py)
- **Expandido**: Agregados los endpoints faltantes (POST, PUT, DELETE, GET búsqueda)
- Todos los endpoints incluyen documentación clara
- Manejo robusto de errores con mensajes descriptivos
- Respuestas consistentes en formato JSON

### 3. [test_main.py](test_main.py)
- **Nuevo archivo**: Suite completa de pruebas unitarias con pytest
- **35 pruebas** cubriendo todos los endpoints
- Validación de casos exitosos y casos de error
- Pruebas de integración para flujos completos

### 4. [API_SPECIFICATION.md](API_SPECIFICATION.md)
- **Nuevo archivo**: Especificación detallada de la API
- Tabla de referencia para cada endpoint (según requisitos)
- Ejemplos de cURL para cada operación
- Documentación de códigos de error

## Instalación

### 1. Clonar el repositorio
```bash
cd /workspaces/Fast_API
```

### 2. Crear entorno virtual (si no existe)
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install fastapi uvicorn sqlite3 pytest httpx
```

### 4. Inicializar la base de datos
```bash
cd apis/contactos
python init_db.py
```

## Ejecución

### Iniciar el servidor FastAPI
```bash
cd /workspaces/Fast_API/apis/contactos
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

El servidor estará disponible en: **http://localhost:8000**

Documentación interactiva: **http://localhost:8000/docs**

### Ejecutar las pruebas unitarias
```bash
cd /workspaces/Fast_API/apis/contactos
python -m pytest test_main.py -v
```

### Ejecutar pruebas con cobertura
```bash
python -m pytest test_main.py --cov=main --cov-report=html
```

## Ejemplos de Uso

### 1. Obtener bienvenida
```bash
curl -X GET http://localhost:8000/
```

### 2. Listar contactos (paginado)
```bash
curl -X GET "http://localhost:8000/v1/contactos?limit=5&skip=0"
```

### 3. Obtener contacto por ID
```bash
curl -X GET http://localhost:8000/v1/contactos/1
```

### 4. Buscar contacto por nombre
```bash
curl -X GET "http://localhost:8000/v1/contacto?nombre=Sophia"
```

### 5. Crear nuevo contacto
```bash
curl -X POST http://localhost:8000/v1/contacto \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Juan Pérez", "telefono": "5551234567", "email": "juan@example.com"}'
```

### 6. Actualizar contacto
```bash
curl -X PUT http://localhost:8000/v1/contacto \
  -H "Content-Type: application/json" \
  -d '{"id_contacto": 1, "nombre": "Juan Actualizado"}'
```

### 7. Eliminar contacto
```bash
curl -X DELETE "http://localhost:8000/v1/contacto?id_contacto=1"
```

## Estructura de Respuestas

### Respuesta Exitosa (200/201)
```json
{
  "table": "contactos",
  "item": {
    "id_contacto": 1,
    "nombre": "Sophia Carey",
    "telefono": "3764327208",
    "email": "gravida@outlook.edu"
  },
  "datetime": "31/03/2026 10:30:15",
  "message": "Contacto encontrado correctamente"
}
```

### Respuesta de Error (400)
```json
{
  "table": "contactos",
  "item": {},
  "datetime": "31/03/2026 10:30:15",
  "message": "El contacto no existe"
}
```

### Respuesta de Listado (200)
```json
{
  "table": "contactos",
  "items": [
    {
      "id_contacto": 1,
      "nombre": "Sophia Carey",
      "telefono": "3764327208",
      "email": "gravida@outlook.edu"
    }
  ],
  "count": 1,
  "total": 100,
  "datetime": "31/03/2026 10:30:15",
  "message": "Datos consultados correctamente",
  "limit": 5,
  "skip": 0
}
```

## Validaciones Implementadas

### GET /v1/contactos
- ✅ Parámetros `limit` y `skip` son obligatorios
- ✅ `limit` debe ser > 0
- ✅ Parámetros no pueden ser negativos

### POST /v1/contacto
- ✅ Campos `nombre`, `telefono`, `email` obligatorios
- ✅ Validación de datos antes de insertar

### PUT /v1/contacto
- ✅ Campo `id_contacto` obligatorio
- ✅ Al menos un campo adicional debe ser actualizado
- ✅ Verifica que el contacto existe antes de actualizar

### DELETE /v1/contacto
- ✅ Parámetro `id_contacto` obligatorio
- ✅ Verifica existencia antes de eliminar

## Pruebas Unitarias (35 tests)

### Cobertura:
- ✅ Endpoint raíz (2 tests)
- ✅ GET /v1/contactos (8 tests)
- ✅ GET /v1/contactos/{id} (3 tests)
- ✅ GET /v1/contacto búsqueda (5 tests)
- ✅ POST /v1/contacto (5 tests)
- ✅ PUT /v1/contacto (5 tests)
- ✅ DELETE /v1/contacto (4 tests)
- ✅ Pruebas de integración (3 tests)

### Resultados
```
======================== 35 passed in 1.78s ========================
```

## Base de Datos

### Tabla: contactos
```sql
CREATE TABLE contactos (
    id_contacto INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    telefono TEXT NOT NULL,
    email TEXT NOT NULL
)
```

### Campos:
- **id_contacto**: Identificador único (INTEGER, PRIMARY KEY)
- **nombre**: Nombre del contacto (TEXT, NOT NULL)
- **telefono**: Teléfono del contacto (TEXT, NOT NULL)
- **email**: Email del contacto (TEXT, NOT NULL)

### Datos Iniciales
Se cargan 100 contactos del archivo `data.csv`

## Información Adicional

### Versión de Dependencias
- **FastAPI**: ^0.100.0
- **Uvicorn**: ^0.23.0
- **Pytest**: ^7.4.0
- **Python**: 3.12.1

### Características de la API
- Documentación automática (Swagger UI) en `/docs`
- Formato de respuesta JSON consistente
- Manejo centralizado de errores
- Timestamp en todas las respuestas
- Paginación para listados

### Notas de Desarrollo
- La API utiliza SQLite como base de datos
- Se respeta el patrón de respuestas consistentes
- Todos los parámetros de búsqueda soportan LIKE para flexibilidad
- Las actualizaciones son parciales (solo los campos enviados)

## Autor
Desarrollo completado el 31/03/2026

## Licencia
MIT
