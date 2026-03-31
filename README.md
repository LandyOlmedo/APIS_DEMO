# 📋 API de Agenda de Contactos

## 📚 Documentación de Endpoints

Esta documentación describe todos los endpoints disponibles en la API REST de contactos.

---

## 1. GET / (Endpoint Raíz)

| No | Propiedad | Detalle |
|----|-----------|---------|
| 1 | Descripción | Endpoint de bienvenida |
| 2 | Summary | Mensaje de bienvenida de la API |
| 3 | Método | GET |
| 4 | Endpoint | `/` |
| 5 | Autenticación | No requerida |
| 6 | Parámetros Query | Ninguno |
| 7 | Parámetros Path | Ninguno |
| 8 | Body/Data | N/A |
| 9 | Status Code | `200 OK` |
| 10 | Content-Type | `application/json` |
| 11 | Status Code Error | N/A |
| 12 | Response |  `{"message": "API de la Agenda", "datetime": "31/03/2026 10:30:15"}` |
| 13 | cURL | `curl -X GET http://127.0.0.1:8000/` |

---

## 2. GET /v1/contactos (Listar Contactos - Paginado)

| No | Propiedad | Detalle |
|----|-----------|---------|
| 1 | Descripción | Obtener lista paginada de contactos |
| 2 | Summary | Endpoint que regresa los contactos paginados |
| 3 | Método | GET |
| 4 | Endpoint | `/v1/contactos` |
| 5 | Autenticación | No requerida |
| 6 | Parámetros Query | `limit` (int, requerido), `skip` (int, requerido) |
| 7 | Parámetros Path | Ninguno |
| 8 | Body/Data | N/A |
| 9 | Status Code | `200 OK` |
| 10 | Content-Type | `application/json` |
| 11 | Status Code Error | `400 Bad Request` |
| 12 | Validaciones | limit > 0, limit >= 0, skip >= 0 |
| 13 | Response | Array de contactos + count + total |
| 14 | cURL | `curl -X GET "http://127.0.0.1:8000/v1/contactos?limit=10&skip=0"` |

**Ejemplo Response (200):**
```json
{
  "table": "contactos",
  "items": [
    {
      "id_contacto": 1,
      "nombre": "María Rodríguez",
      "telefono": "0005550001",
      "email": "contacto1@example.com"
    }
  ],
  "count": 1,
  "total": 100,
  "datetime": "31/03/2026 10:30:15",
  "message": "Datos consultados correctamente"
}
```

---

## 3. GET /v1/contactos/{id_contacto} (Obtener Contacto por ID)

| No | Propiedad | Detalle |
|----|-----------|---------|
| 1 | Descripción | Obtener un contacto específico por ID |
| 2 | Summary | Consultar un contacto por su ID |
| 3 | Método | GET |
| 4 | Endpoint | `/v1/contactos/{id_contacto}` |
| 5 | Autenticación | No requerida |
| 6 | Parámetros Query | Ninguno |
| 7 | Parámetros Path | `id_contacto` (int, requerido) |
| 8 | Body/Data | N/A |
| 9 | Status Code | `200 OK` |
| 10 | Content-Type | `application/json` |
| 11 | Status Code Error | `400 Not Found` |
| 12 | Validaciones | id_contacto debe existir en BD |
| 13 | Response | Objeto contacto o error |
| 14 | cURL | `curl -X GET http://127.0.0.1:8000/v1/contactos/1` |

**Ejemplo Response (200):**
```json
{
  "table": "contactos",
  "item": {
    "id_contacto": 1,
    "nombre": "María Rodríguez",
    "telefono": "0005550001",
    "email": "contacto1@example.com"
  },
  "datetime": "31/03/2026 10:30:15",
  "message": "Contacto encontrado correctamente"
}
```

---

## 4. GET /v1/contacto (Buscar Contacto)

| No | Propiedad | Detalle |
|----|-----------|---------|
| 1 | Descripción | Buscar contacto por nombre o ID |
| 2 | Summary | Búsqueda dinámica de contactos |
| 3 | Método | GET |
| 4 | Endpoint | `/v1/contacto` |
| 5 | Autenticación | No requerida |
| 6 | Parámetros Query | `nombre` (opcional) O `id_contacto` (opcional) - uno requerido |
| 7 | Parámetros Path | Ninguno |
| 8 | Body/Data | N/A |
| 9 | Status Code | `200 OK` |
| 10 | Content-Type | `application/json` |
| 11 | Status Code Error | `400 Bad Request` / `404 Not Found` |
| 12 | Validaciones | Debe enviar nombre O id_contacto |
| 13 | Response | Objeto contacto encontrado |
| 14 | cURL | `curl -X GET "http://127.0.0.1:8000/v1/contacto?nombre=Juan"` |

**Ejemplo Response (200):**
```json
{
  "table": "contactos",
  "item": {
    "id_contacto": 5,
    "nombre": "Juan Pérez",
    "telefono": "5551234567",
    "email": "juan@example.com"
  },
  "datetime": "31/03/2026 10:30:15",
  "message": "Contacto encontrado correctamente"
}
```

---

## 5. POST /v1/contacto (Crear Contacto)

| No | Propiedad | Detalle |
|----|-----------|---------|
| 1 | Descripción | Crear un nuevo contacto |
| 2 | Summary | Insertar nuevo contacto en la BD |
| 3 | Método | POST |
| 4 | Endpoint | `/v1/contacto` |
| 5 | Autenticación | No requerida |
| 6 | Parámetros Query | Ninguno |
| 7 | Parámetros Path | Ninguno |
| 8 | Body/Data | Form fields: `nombre`, `telefono`, `email` |
| 9 | Content-Type | `application/x-www-form-urlencoded` |
| 10 | Status Code | `201 Created` |
| 11 | Status Code Error | `422 Unprocessable Entity` |
| 12 | Validaciones | Todos campos requeridos, nombres 1-100 chars, teléfono 7-20 chars |
| 13 | Response | Contacto creado con ID generado |
| 14 | cURL | `curl -X POST http://127.0.0.1:8000/v1/contacto -d "nombre=Carlos&telefono=5551234567&email=carlos@example.com"` |

**Validaciones de Campos:**

| Campo | Tipo | Mín | Máx | Requerido |
|-------|------|-----|-----|-----------|
| nombre | string | 1 | 100 | ✅ |
| telefono | string | 7 | 20 | ✅ |
| email | string | - | - | ✅ |

**Ejemplo Response (201):**
```json
{
  "table": "contactos",
  "item": {
    "id_contacto": 163,
    "nombre": "Carlos Nuevo",
    "telefono": "5559876543",
    "email": "carlos@example.com"
  },
  "datetime": "31/03/2026 10:30:15",
  "message": "Contacto creado correctamente"
}
```

---

## 6. PUT /v1/contacto (Actualizar Contacto)

| No | Propiedad | Detalle |
|----|-----------|---------|
| 1 | Descripción | Actualizar contacto existente |
| 2 | Summary | Modificar datos de contacto |
| 3 | Método | PUT |
| 4 | Endpoint | `/v1/contacto` |
| 5 | Autenticación | No requerida |
| 6 | Parámetros Query | Ninguno |
| 7 | Parámetros Path | Ninguno |
| 8 | Body/Data | Form fields: `id_contacto` (requerido), resto opcionales |
| 9 | Content-Type | `application/x-www-form-urlencoded` |
| 10 | Status Code | `200 OK` |
| 11 | Status Code Error | `400 Bad Request` / `422 Unprocessable` |
| 12 | Validaciones | id_contacto > 0, debe existir, al menos 1 campo para actualizar |
| 13 | Response | Contacto actualizado |
| 14 | cURL | `curl -X PUT http://127.0.0.1:8000/v1/contacto -d "id_contacto=163&nombre=Carlos%20Actualizado"` |

**Validaciones de Campos:**

| Campo | Tipo | Mín | Máx | Requerido | Notas |
|-------|------|-----|-----|-----------|-------|
| id_contacto | int | - | - | ✅ | > 0, debe existir |
| nombre | string | 1 | 100 | ❌ | Opcional |
| telefono | string | 7 | 20 | ❌ | Opcional |
| email | string | - | - | ❌ | Opcional |

**Ejemplo Response (200):**
```json
{
  "table": "contactos",
  "item": {
    "id_contacto": 163,
    "nombre": "Carlos Actualizado",
    "telefono": "5551111111",
    "email": "carlos@nuevo.com"
  },
  "datetime": "31/03/2026 10:30:15",
  "message": "Contacto actualizado correctamente"
}
```

---

## 7. DELETE /v1/contacto (Eliminar Contacto)

| No | Propiedad | Detalle |
|----|-----------|---------|
| 1 | Descripción | Eliminar un contacto |
| 2 | Summary | Borrar contacto de la BD |
| 3 | Método | DELETE |
| 4 | Endpoint | `/v1/contacto` |
| 5 | Autenticación | No requerida |
| 6 | Parámetros Query | `id_contacto` (int, requerido) |
| 7 | Parámetros Path | Ninguno |
| 8 | Body/Data | N/A |
| 9 | Status Code | `200 OK` |
| 10 | Content-Type | `application/json` |
| 11 | Status Code Error | `400 Not Found` |
| 12 | Validaciones | id_contacto debe existir en BD |
| 13 | Response | Mensaje de confirmación |
| 14 | cURL | `curl -X DELETE "http://127.0.0.1:8000/v1/contacto?id_contacto=163"` |

**Ejemplo Response (200):**
```json
{
  "table": "contactos",
  "datetime": "31/03/2026 10:30:15",
  "message": "Contacto eliminado correctamente"
}
```

---

## 🗄️ Esquema de Base de Datos

### Tabla: contactos

| Campo | Tipo | Constraints | Descripción |
|-------|------|-------------|-------------|
| id_contacto | INTEGER | PRIMARY KEY, AUTO INCREMENT | Identificador único del contacto |
| nombre | TEXT | NOT NULL, 1-100 caracteres | Nombre completo del contacto |
| telefono | TEXT | NOT NULL, 7-20 caracteres | Número telefónico |
| email | TEXT | NOT NULL | Correo electrónico |

**SQL (DDL):**
```sql
CREATE TABLE contactos (
    id_contacto INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    telefono TEXT NOT NULL,
    email TEXT NOT NULL
)
```

---

## 📊 Resumen de Endpoints

| # | Método | Endpoint | Descripción | Status |
|---|--------|----------|-------------|--------|
| 1 | GET | `/` | Raíz - Mensaje de bienvenida | `200` |
| 2 | GET | `/v1/contactos` | Listar contactos (paginado) | `200` / `400` |
| 3 | GET | `/v1/contactos/{id}` | Obtener contacto por ID | `200` / `400` |
| 4 | GET | `/v1/contacto` | Buscar por nombre o ID | `200` / `400` |
| 5 | POST | `/v1/contacto` | Crear nuevo contacto | `201` / `422` |
| 6 | PUT | `/v1/contacto` | Actualizar contacto | `200` / `400` / `422` |
| 7 | DELETE | `/v1/contacto` | Eliminar contacto | `200` / `400` |

---
    TODO: Responder la peticion

