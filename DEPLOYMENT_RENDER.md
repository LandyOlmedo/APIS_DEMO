# Guía de Despliegue en Render

## Archivos de Configuración Creados

✅ **Procfile** - Define cómo Render debe ejecutar la aplicación
✅ **render.yaml** - Configuración alternativa para Render
✅ **runtime.txt** - Especifica la versión de Python (3.11.9)
✅ **.env.example** - Ejemplo de variables de entorno
✅ **.gitignore** - Archivos gitignored para no subir a repositorio

## Paso a Paso para Desplegar en Render

### 1️⃣ **Preparar el Repositorio en GitHub**

```bash
# Asegúrate de que todos los cambios estén en GitHub
git add .
git commit -m "Configure for Render deployment"
git push origin main
```

### 2️⃣ **Conectar Render con GitHub**

1. Ve a [https://dashboard.render.com](https://dashboard.render.com)
2. Haz clic en **"New +"** → **"Web Service"**
3. Selecciona **"Connect a repository"**
4. Busca tu repositorio: **LandyOlmedo/APIS_DEMO**
5. Haz clic en **"Connect"**

### 3️⃣ **Configurar el Servicio Web**

Rellena los siguientes campos:

| Campo | Valor |
|-------|-------|
| **Name** | `fastapi-contactos-api` |
| **Environment** | `Python` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn apis.contactos.main:app --host 0.0.0.0 --port $PORT` |
| **Plan** | `Free` |

### 4️⃣ **Variables de Entorno (opcional)**

En la sección **Environment** agrega:
- `PYTHON_VERSION`: `3.11`
- `DEBUG`: `False`

### 5️⃣ **Desplegar**

1. Haz clic en **"Create Web Service"**
2. Render automáticamente:
   - Clonar el repositorio
   - Instalar dependencias (`pip install -r requirements.txt`)
   - Ejecutar el Procfile
   - Asignar una URL públi

## URL del Servicio

Una vez desplegado, podrás acceder en:

```
https://fastapi-contactos-api.onrender.com
```

## Endpoints Disponibles

- **Health Check**: `GET /`
  ```bash
  curl -X GET https://fastapi-contactos-api.onrender.com/
  ```

- **Obtener Contactos**: `GET /v1/contactos?limit=10&skip=0`
  ```bash
  curl -X GET "https://fastapi-contactos-api.onrender.com/v1/contactos?limit=10&skip=0"
  ```

- **Documentación Interactiva**: 
  - Swagger UI: `https://fastapi-contactos-api.onrender.com/docs`
  - ReDoc: `https://fastapi-contactos-api.onrender.com/redoc`

## ⚠️ Consideraciones Importantes

### Base de Datos SQLite
- La base de datos `agendadb.sqlite3` se **eliminará** cada vez que Render redepliegue
- Para persistencia real, migra a:
  - **PostgreSQL** (recomendado en Render)
  - **MongoDB**
  - **SQLAlchemy** con base de datos externa

### Tiempo de Inactividad (Plan Free)
- La aplicación se suspenderá después de **15 minutos de inactividad**
- El primer acceso después de la suspensión tardará 30-50 segundos
- Para evitar esto, usa un plan de pago

### Logs
- Ver logs en tiempo real en Render Dashboard
- O mediante CLI: `render logs <service-id>`

## Actualizar la Aplicación

Cada vez que hagas `push` a GitHub en la rama `main`:

```bash
git add .
git commit -m "Update API"
git push origin main
```

**Render automáticamente redesplegará** la aplicación con los cambios nuevos.

## Troubleshooting

### ❌ Error: "ModuleNotFoundError"
- Verifica que los imports en `main.py` sean correctos
- Asegúrate de que `APIs` sea ejecutable (añade `__init__.py`)

### ❌ Error: "Port already in use"
- El Procfile ya usa `$PORT` que Render asigna dinámicamente
- No hardcodees puertos locales

### ❌ Base de datos no encontrada
- Actualiza el `init_db.py` para crear la BD si no existe
- O implementa una migración automática en el startup

## Recursos
- [Documentación oficial de Render](https://render.com/docs)
- [FastAPI en Render](https://render.com/docs/deploy-fastapi)
- [Variables de entorno en Render](https://render.com/docs/environment-variables)
