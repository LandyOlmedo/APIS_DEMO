# Guía de Pruebas en Postman - API de Contactos

## ⚠️ Problema común: 404 Not Found

Si obtienes **"404 Not Found"**, probablemente:
- ❌ No estás usando `/v1/` en la URL
- ❌ Escribiste mal la ruta
- ❌ El servidor no está running

## ✅ Verificar que el servidor está ejecutando

**En terminal (en la carpeta apis/contactos):**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Deberías ver:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

## 📋 Todos los Endpoints Disponibles

### 1️⃣ GET / - Raíz (Bienvenida)

| Campo | Valor |
|-------|-------|
| **Método** | GET |
| **URL** | `http://localhost:8000/` |
| **Headers** | No requeridos |
| **Body** | Vacío |
| **Status esperado** | 200 |

**Respuesta:**
```json
{
  "message": "API de la Agenda",
  "datetime": "31/03/2026 10:30:15"
}
```

---

### 2️⃣ GET /v1/contactos - Listar contactos (Paginado)

| Campo | Valor |
|-------|-------|
| **Método** | GET |
| **URL** | `http://localhost:8000/v1/contactos?limit=5&skip=0` |
| **Headers** | No requeridos |
| **Query Params** | `limit=5` (obligatorio)<br>`skip=0` (obligatorio) |
| **Body** | Vacío |
| **Status esperado** | 200 |

**Ejemplo de URL completa:**
```
http://localhost:8000/v1/contactos?limit=10&skip=0
```

**Respuesta:**
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
  "limit": 10,
  "skip": 0
}
```

---

### 3️⃣ GET /v1/contactos/{id} - Obtener contacto por ID

| Campo | Valor |
|-------|-------|
| **Método** | GET |
| **URL** | `http://localhost:8000/v1/contactos/1` |
| **Headers** | No requeridos |
| **Path param** | `id=1` (reemplaza 1 con el ID) |
| **Body** | Vacío |
| **Status esperado** | 200 o 400 si no existe |

**Ejemplos válidos:**
- `http://localhost:8000/v1/contactos/1`
- `http://localhost:8000/v1/contactos/5`
- `http://localhost:8000/v1/contactos/100`

**Respuesta (éxito):**
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

**Respuesta (error - no existe):**
```json
{
  "table": "contactos",
  "item": {},
  "datetime": "31/03/2026 10:30:15",
  "message": "El contacto no existe"
}
```

---

### 4️⃣ GET /v1/contacto - Buscar por nombre o ID (Query params)

| Campo | Valor |
|-------|-------|
| **Método** | GET |
| **URL** | `http://localhost:8000/v1/contacto?nombre=Sophia` |
| **Headers** | No requeridos |
| **Query Params** | `nombre=Sophia` O `id_contacto=1` (al menos uno) |
| **Body** | Vacío |
| **Status esperado** | 200 o 400 |

**Ejemplos válidos:**

**Por nombre:**
```
http://localhost:8000/v1/contacto?nombre=Sophia
http://localhost:8000/v1/contacto?nombre=Whitney
http://localhost:8000/v1/contacto?nombre=Juan
```

**Por ID:**
```
http://localhost:8000/v1/contacto?id_contacto=1
http://localhost:8000/v1/contacto?id_contacto=5
```

**Respuesta:**
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

---

### 5️⃣ POST /v1/contacto - Crear nuevo contacto

| Campo | Valor |
|-------|-------|
| **Método** | POST |
| **URL** | `http://localhost:8000/v1/contacto` |
| **Headers** | `Content-Type: application/json` |
| **Body** | JSON (ver abajo) |
| **Status esperado** | 201 (o 400 si falta algún campo) |

**Body (JSON):**
```json
{
  "nombre": "Juan Pérez",
  "telefono": "5551234567",
  "email": "juan@example.com"
}
```

**Respuesta (éxito - Status 201):**
```json
{
  "table": "contactos",
  "item": {
    "id_contacto": 101,
    "nombre": "Juan Pérez",
    "telefono": "5551234567",
    "email": "juan@example.com"
  },
  "datetime": "31/03/2026 10:30:15",
  "message": "Contacto creado correctamente"
}
```

---

### 6️⃣ PUT /v1/contacto - Modificar contacto

| Campo | Valor |
|-------|-------|
| **Método** | PUT |
| **URL** | `http://localhost:8000/v1/contacto` |
| **Headers** | `Content-Type: application/json` |
| **Body** | JSON (ver abajo) |
| **Status esperado** | 200 (o 400 si falta id o no existe) |

**Body (JSON) - Campos opcionales:**
```json
{
  "id_contacto": 1,
  "nombre": "Nuevo Nombre",
  "telefono": "9999999999",
  "email": "nuevo@email.com"
}
```

**Nota:** El campo `id_contacto` es obligatorio. Los otros son opcionales.

**Ejemplos válidos:**

Actualizar solo nombre:
```json
{
  "id_contacto": 1,
  "nombre": "Sophia Actualizado"
}
```

Actualizar solo email:
```json
{
  "id_contacto": 1,
  "email": "newemail@example.com"
}
```

Actualizar todo:
```json
{
  "id_contacto": 1,
  "nombre": "Nuevo Nombre",
  "telefono": "1234567890",
  "email": "nuevo@example.com"
}
```

**Respuesta (éxito):**
```json
{
  "table": "contactos",
  "item": {
    "id_contacto": 1,
    "nombre": "Nuevo Nombre",
    "telefono": "1234567890",
    "email": "nuevo@example.com"
  },
  "datetime": "31/03/2026 10:30:15",
  "message": "Contacto actualizado correctamente"
}
```

---

### 7️⃣ DELETE /v1/contacto - Eliminar contacto

| Campo | Valor |
|-------|-------|
| **Método** | DELETE |
| **URL** | `http://localhost:8000/v1/contacto?id_contacto=1` |
| **Headers** | No requeridos |
| **Query Params** | `id_contacto=1` (obligatorio) |
| **Body** | Vacío |
| **Status esperado** | 200 (o 400 si no existe) |

**Ejemplos válidos:**
```
http://localhost:8000/v1/contacto?id_contacto=1
http://localhost:8000/v1/contacto?id_contacto=101
```

**Respuesta (éxito):**
```json
{
  "table": "contactos",
  "datetime": "31/03/2026 10:30:15",
  "message": "Contacto eliminado correctamente"
}
```

---

## 🔴 Errores Comunes en Postman

### ❌ Error: 404 Not Found

**Causa:** URL incorrecta o mala ruta

**Soluciones:**
✅ Asegúrate de usar `/v1/` en la ruta  
✅ Verifica la ortografía  
✅ URL correcta: `http://localhost:8000/v1/contactos`  
❌ URL incorrecta: `http://localhost:8000/contactos`  
❌ URL incorrecta: `http://localhost:8000/v1/contacto/lista`  

### ❌ Error: 400 Bad Request

**Causa:** Parámetros faltantes o inválidos

**Soluciones:**
✅ GET /v1/contactos requiere `limit` Y `skip`  
✅ POST /v1/contacto requiere `nombre`, `telefono` y `email`  
✅ PUT /v1/contacto requiere `id_contacto` y al menos un campo más  
✅ DELETE /v1/contacto requiere `id_contacto` en query params  

### ❌ Error: 500 Internal Server Error

**Causa:** Error en el servidor

**Soluciones:**
✅ Revisa que el servidor esté ejecutando  
✅ Revisa la terminal donde ejecutaste uvicorn  

---

## 📝 Pasos para configurar cada prueba en Postman

### GET /v1/contactos

1. **Abre Postman** y crea nueva request
2. **Método:** GET
3. **URL:** `http://localhost:8000/v1/contactos`
4. **Params tab:**
   - Key: `limit` | Value: `5`
   - Key: `skip` | Value: `0`
5. Haz clic en **Send**

### POST /v1/contacto

1. **Método:** POST
2. **URL:** `http://localhost:8000/v1/contacto`
3. **Headers tab:**
   - Key: `Content-Type` | Value: `application/json`
4. **Body tab:** Selecciona **raw** y **JSON**
5. Pega el JSON:
```json
{
  "nombre": "Test User",
  "telefono": "5551234567",
  "email": "test@example.com"
}
```
6. Haz clic en **Send**

---

## 🎯 URLs Rápidas para Copiar-Pegar

```
GET raíz:
http://localhost:8000/

GET contactos (paginado):
http://localhost:8000/v1/contactos?limit=10&skip=0

GET contacto por ID:
http://localhost:8000/v1/contactos/1

GET búsqueda por nombre:
http://localhost:8000/v1/contacto?nombre=Sophia

GET búsqueda por ID:
http://localhost:8000/v1/contacto?id_contacto=1

POST crear:
http://localhost:8000/v1/contacto

PUT actualizar:
http://localhost:8000/v1/contacto

DELETE eliminar:
http://localhost:8000/v1/contacto?id_contacto=1
```

---

## 📚 Documentación interactiva

También puedes usar **Swagger UI** para probar directamente en el navegador:

```
http://localhost:8000/docs
```

Ahí puedes ver todos los endpoints con documentación automática. ¡Recomendado! 🚀
