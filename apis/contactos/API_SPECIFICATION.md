# Especificación de API REST - Agenda de Contactos

## 1. GET / - Endpoint Raíz (Root)

| Propiedad | Detalle |
|-----------|---------|
| **Description** | Endpoint que da bienvenida a la API |
| **Summary** | Endpoint de raíz |
| **Version** | 1.0 |
| **Method** | GET |
| **Endpoint** | `/` |
| **Authentication** | No requerida |
| **Query param** | No aplica |
| **Path param** | No aplica |
| **Data** | No aplica (GET sin body) |
| **Status code** | 200 |
| **Response type** | application/json |
| **Response** | `{"message": "API de la Agenda", "datetime": "31/03/2026 10:30:15"}` |
| **Status code (error)** | N/A |
| **Response type (error)** | N/A |
| **Response (error)** | N/A |
| **cURL** | `curl -X GET http://localhost:8000/` |
| **Table** | Ninguna |

---

## 2. GET /v1/contactos - Listar Contactos con Paginación

| Propiedad | Detalle |
|-----------|---------|
| **Description** | Endpoint que regresa una lista de contactos paginados |
| **Summary** | Endpoint de contactos |
| **Version** | 1.0 |
| **Method** | GET |
| **Endpoint** | `/v1/contactos` |
| **Authentication** | No requerida |
| **Query param** | `limit` (int, obligatorio) - Número de registros a regresar<br>`skip` (int, obligatorio) - Número de registros a omitir |
| **Path param** | No aplica |
| **Data** | No aplica (GET sin body) |
| **Status code** | 200 |
| **Response type** | application/json |
| **Response** | `{"table": "contactos", "items": [{id_contacto, nombre, telefono, email}, ...], "count": 5, "total": 100, "datetime": "31/03/2026 10:30:15", "message": "Datos consultados correctamente", "limit": 5, "skip": 0}` |
| **Status code (error)** | 400 |
| **Response type (error)** | application/json |
| **Response (error)** | `{"table": "contactos", "items": [], "count": 0, "total": 0, "datetime": "31/03/2026 10:30:15", "message": "Debes enviar los parámetros 'limit' y 'skip'", "limit": null, "skip": null}` |
| **cURL** | `curl -X GET "http://localhost:8000/v1/contactos?limit=5&skip=0"` |
| **Table** | contactos |

---

## 3. GET /v1/contactos/{id_contacto} - Obtener Contacto por ID

| Propiedad | Detalle |
|-----------|---------|
| **Description** | Endpoint que regresa un contacto específico por su ID |
| **Summary** | Consultar un contacto por ID |
| **Version** | 1.0 |
| **Method** | GET |
| **Endpoint** | `/v1/contactos/{id_contacto}` |
| **Authentication** | No requerida |
| **Query param** | No aplica |
| **Path param** | `id_contacto` (int, obligatorio) - ID del contacto a consultar |
| **Data** | No aplica (GET sin body) |
| **Status code** | 200 |
| **Response type** | application/json |
| **Response** | `{"table": "contactos", "item": {id_contacto, nombre, telefono, email}, "datetime": "31/03/2026 10:30:15", "message": "Contacto encontrado correctamente"}` |
| **Status code (error)** | 400 |
| **Response type (error)** | application/json |
| **Response (error)** | `{"table": "contactos", "item": {}, "datetime": "31/03/2026 10:30:15", "message": "El contacto no existe"}` |
| **cURL** | `curl -X GET http://localhost:8000/v1/contactos/1` |
| **Table** | contactos |

---

## 4. GET /v1/contacto - Buscar Contacto por Nombre o ID

| Propiedad | Detalle |
|-----------|---------|
| **Description** | Endpoint que busca un contacto por nombre o ID |
| **Summary** | Buscar un contacto por nombre o ID |
| **Version** | 1.0 |
| **Method** | GET |
| **Endpoint** | `/v1/contacto` |
| **Authentication** | No requerida |
| **Query param** | `nombre` (string, opcional) - Nombre del contacto a buscar<br>`id_contacto` (int, opcional) - ID del contacto a buscar |
| **Path param** | No aplica |
| **Data** | No aplica (GET sin body) |
| **Status code** | 200 |
| **Response type** | application/json |
| **Response** | `{"table": "contactos", "item": {id_contacto, nombre, telefono, email}, "datetime": "31/03/2026 10:30:15", "message": "Contacto encontrado correctamente"}` |
| **Status code (error)** | 400 |
| **Response type (error)** | application/json |
| **Response (error)** | `{"table": "contactos", "item": {}, "datetime": "31/03/2026 10:30:15", "message": "El contacto no existe"}` |
| **cURL** | `curl -X GET "http://localhost:8000/v1/contacto?nombre=Sophia"` o `curl -X GET "http://localhost:8000/v1/contacto?id_contacto=1"` |
| **Table** | contactos |

---

## 5. POST /v1/contacto - Crear Nuevo Contacto

| Propiedad | Detalle |
|-----------|---------|
| **Description** | Endpoint para insertar un nuevo contacto |
| **Summary** | Crear un nuevo contacto |
| **Version** | 1.0 |
| **Method** | POST |
| **Endpoint** | `/v1/contacto` |
| **Authentication** | No requerida |
| **Query param** | No aplica |
| **Path param** | No aplica |
| **Data** | JSON: `{"nombre": "string", "telefono": "string", "email": "string"}` |
| **Status code** | 201 |
| **Response type** | application/json |
| **Response** | `{"table": "contactos", "item": {id_contacto, nombre, telefono, email}, "datetime": "31/03/2026 10:30:15", "message": "Contacto creado correctamente"}` |
| **Status code (error)** | 400 |
| **Response type (error)** | application/json |
| **Response (error)** | `{"table": "contactos", "item": {}, "datetime": "31/03/2026 10:30:15", "message": "Faltan campos requeridos: nombre, telefono, email"}` |
| **cURL** | `curl -X POST http://localhost:8000/v1/contacto -H "Content-Type: application/json" -d '{"nombre": "Juan Pérez", "telefono": "5551234567", "email": "juan@example.com"}'` |
| **Table** | contactos |

---

## 6. PUT /v1/contacto - Modificar Contacto

| Propiedad | Detalle |
|-----------|---------|
| **Description** | Endpoint para actualizar los datos de un contacto existente |
| **Summary** | Modificar un contacto |
| **Version** | 1.0 |
| **Method** | PUT |
| **Endpoint** | `/v1/contacto` |
| **Authentication** | No requerida |
| **Query param** | No aplica |
| **Path param** | No aplica |
| **Data** | JSON: `{"id_contacto": int, "nombre": "string (opcional)", "telefono": "string (opcional)", "email": "string (opcional)"}` |
| **Status code** | 200 |
| **Response type** | application/json |
| **Response** | `{"table": "contactos", "item": {id_contacto, nombre, telefono, email}, "datetime": "31/03/2026 10:30:15", "message": "Contacto actualizado correctamente"}` |
| **Status code (error)** | 400 |
| **Response type (error)** | application/json |
| **Response (error)** | `{"table": "contactos", "item": {}, "datetime": "31/03/2026 10:30:15", "message": "El contacto no existe"}` |
| **cURL** | `curl -X PUT http://localhost:8000/v1/contacto -H "Content-Type: application/json" -d '{"id_contacto": 1, "nombre": "Juan Pérez Actualizado", "email": "nuevo@example.com"}'` |
| **Table** | contactos |

---

## 7. DELETE /v1/contacto - Eliminar Contacto

| Propiedad | Detalle |
|-----------|---------|
| **Description** | Endpoint para eliminar un contacto por su ID |
| **Summary** | Eliminar un contacto |
| **Version** | 1.0 |
| **Method** | DELETE |
| **Endpoint** | `/v1/contacto` |
| **Authentication** | No requerida |
| **Query param** | `id_contacto` (int, obligatorio) - ID del contacto a eliminar |
| **Path param** | No aplica |
| **Data** | No aplica (DELETE sin body) |
| **Status code** | 200 |
| **Response type** | application/json |
| **Response** | `{"table": "contactos", "datetime": "31/03/2026 10:30:15", "message": "Contacto eliminado correctamente"}` |
| **Status code (error)** | 400 |
| **Response type (error)** | application/json |
| **Response (error)** | `{"table": "contactos", "datetime": "31/03/2026 10:30:15", "message": "El contacto no existe"}` |
| **cURL** | `curl -X DELETE "http://localhost:8000/v1/contacto?id_contacto=1"` |
| **Table** | contactos |

---

## Tabla de Base de Datos: contactos

```sql
CREATE TABLE contactos (
    id_contacto INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    telefono TEXT NOT NULL,
    email TEXT NOT NULL
)
```

### Campos:
- **id_contacto**: Identificador único (PRIMARY KEY)
- **nombre**: Nombre del contacto (texto, obligatorio)
- **telefono**: Teléfono del contacto (texto, obligatorio)
- **email**: Email del contacto (texto, obligatorio)

---

## Notas Importantes

1. **Formato de Fecha/Hora**: Todas las respuestas incluyen `datetime` en formato `DD/MM/YYYY HH:MM:SS`
2. **Códigos HTTP**: 
   - `200`: Éxito en GET, PUT, DELETE
   - `201`: Éxito en POST (creación)
   - `400`: Error en la solicitud
3. **Paginación**: Los parámetros `limit` y `skip` son obligatorios en GET /v1/contactos
4. **Búsqueda**: GET /v1/contacto requiere al menos `nombre` o `id_contacto`
5. **Actualización**: PUT /v1/contacto requiere `id_contacto` y al menos un campo adicional a actualizar
6. **Eliminación**: DELETE /v1/contacto requiere parámetro query `id_contacto`
