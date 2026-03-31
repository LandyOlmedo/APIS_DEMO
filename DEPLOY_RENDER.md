# Guía de despliegue en Render - API FastAPI de Contactos

Esta guía te ayudará a desplegar tu API FastAPI de gestión de contactos en Render.

## Requisitos previos

1. ✅ Repositorio en GitHub (LandyOlmedo/APIS_DEMO)
2. ✅ Cuenta en [https://render.com](https://render.com)
3. ✅ Archivos de configuración listos:
   - `render.yaml` ✅
   - `Procfile` ✅
   - `requirements.txt` ✅

## Pasos para desplegar

### 1. Conectar GitHub a Render

1. Ve a [https://render.com](https://render.com) e inicia sesión
2. Haz clic en **"New +"** → **"Web Service"**
3. Selecciona **"Connect a GitHub repository"**
4. Autoriza Render para acceder a tu GitHub
5. Busca y selecciona el repositorio `APIS_DEMO`

### 2. Configurar el servicio

En el formulario de creación del Web Service, configura:

| Parámetro | Valor |
|-----------|-------|
| **Name** | `fastapi-contactos-api` |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn apis.contactos.main:app --host 0.0.0.0 --port $PORT` |
| **Plan** | `Free` (para desarrollo/pruebas) |
| **Region** | `Ohio` o la más cercana |

### 3. Variables de entorno (opcional)

Si necesitas variables de entorno, agrégalas en la sección **"Environment"**:
```
DEBUG=False
ENVIRONMENT=production
```

### 4. Desplegar

1. Haz clic en **"Create Web Service"**
2. Render comenzará a construir e instalar dependencias
3. Luego desplegará la aplicación
4. Espera a que el estado cambie a **"Live"** (puede tardar 2-5 minutos)

## URL de la API después del despliegue

Una vez desplegada, tu API estará disponible en:

```
https://fastapi-contactos-api.onrender.com
```

## Documentación interactiva

Accede a Swagger UI en:

```
https://fastapi-contactos-api.onrender.com/docs
```

## Endpoints disponibles

### 1. GET / - Raíz (Bienvenida)
```bash
curl https://fastapi-contactos-api.onrender.com/
```

Respuesta:
```json
{
  "message": "API de la Agenda",
  "datetime": "31/03/2026 10:30:15"
}
```

### 2. GET /v1/contactos - Listar contactos (Paginado)
```bash
curl "https://fastapi-contactos-api.onrender.com/v1/contactos?limit=10&skip=0"
```

Parámetros requeridos:
- `limit` (int): número de registros a retornar
- `skip` (int): número de registros a saltar

Respuesta:
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

### 3. GET /v1/contactos/{id_contacto} - Obtener contacto por ID
```bash
curl https://fastapi-contactos-api.onrender.com/v1/contactos/1
```

Respuesta:
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

### 4. GET /v1/contacto - Buscar por nombre o ID
```bash
# Por nombre
curl "https://fastapi-contactos-api.onrender.com/v1/contacto?nombre=Sophia"

# Por ID
curl "https://fastapi-contactos-api.onrender.com/v1/contacto?id_contacto=1"
```

### 5. POST /v1/contacto - Crear nuevo contacto
```bash
curl -X POST https://fastapi-contactos-api.onrender.com/v1/contacto \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Pérez",
    "telefono": "5551234567",
    "email": "juan@example.com"
  }'
```

Respuesta (Status: 201):
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

### 6. PUT /v1/contacto - Modificar contacto
```bash
curl -X PUT https://fastapi-contactos-api.onrender.com/v1/contacto \
  -H "Content-Type: application/json" \
  -d '{
    "id_contacto": 1,
    "nombre": "Sophia Actualizado",
    "email": "nuevo@example.com"
  }'
```

### 7. DELETE /v1/contacto - Eliminar contacto
```bash
curl -X DELETE "https://fastapi-contactos-api.onrender.com/v1/contacto?id_contacto=101"
```

Respuesta (Status: 200):
```json
{
  "table": "contactos",
  "datetime": "31/03/2026 10:30:15",
  "message": "Contacto eliminado correctamente"
}
```

## Solución de problemas

### Problema: "Build failed"
**Solución:** Verifica que:
- `requirements.txt` exista y tenga dependencias válidas
- No haya archivos `.pyc` innecesarios
- La sintaxis de Python sea correcta

### Problema: "Application startup failed"
**Solución:** Comprueba:
- El comando `Start Command` sea correcto
- Los archivos `init_db.py` y `main.py` existan en `apis/contactos/`
- No haya errores de importación

### Problema: "Cannot find module"
**Solución:**
- La importación debe ser desde el directorio raíz del proyecto
- Ruta correcta: `apis.contactos.main:app`

## Monitoreo del despliegue

En el dashboard de Render puedes:
1. Ver los logs en tiempo real
2. Monitorear el uso de CPU y memoria
3. Reiniciar el servicio si es necesario
4. Ver el estado de "Live", "Building" o "Failed"

## Referencias

- [Documentación de Render](https://render.com/docs)
- [Documentación de FastAPI](https://fastapi.tiangolo.com/)
- [GitHub Repository](https://github.com/LandyOlmedo/APIS_DEMO)

## Notas importantes

- El plan **Free** de Render apaga la aplicación después de 15 minutos sin solicitudes
- Para producción, considera usar un plan **Paid** o **Pro**
- La base de datos SQLite se reinicia con cada despliegue (considera usar una BD externa para producción)
- Todos los endpoints están documentados en `/docs` con Swagger UI
https://fastapi-agenda.onrender.com/docs
```

Aquí puedes probar todos los endpoints directamente desde el navegador.

## Notas importantes

### Plan Free
- La aplicación se "duerme" después de 15 minutos de inactividad
- Primera solicitud después de dormir tardará más tiempo (~30 segundos)
- Actualiza a un plan pagado si necesitas disponibilidad 24/7

### Base de datos SQLite
- La BD se inicializa automáticamente al desplegar
- Se crean 100 registros de ejemplo
- Los datos persisten entre reinicios (mientras el contenedor no se elimine)
- **ADVERTENCIA**: Si Render elimina el contenedor, los datos se pierden

### Para producción
Considera usar PostgreSQL o MongoDB en lugar de SQLite:
1. Agrega una base de datos desde Render
2. Configura la cadena de conexión como variable de entorno
3. Actualiza tu código para conectarse a la BD externa

## Solución de problemas

### La app se despliega pero no funciona

1. Revisa los logs en el dashboard de Render
2. Verifica que `requirements.txt` tenga todas las dependencias
3. Confirma que `apis/contactos/main.py` existe

### Error "Build failed"

- Verifica que no haya errores de sintaxis en Python
- Asegúrate de que todos los imports están disponibles
- Comprueba el archivo `requirements.txt`

### API lenta o timeout

- El plan Free tiene recursos limitados
- Espera el reinicio automático
- Considera actualizar a un plan pagado

## Próximos pasos

- ✅ Agrega más endpoints según sea necesario
- ✅ Implementa autenticación (JWT, OAuth2)
- ✅ Migra a una BD más robusta
- ✅ Configura CI/CD con GitHub Actions
- ✅ Monitorea con Sentry o similar

¡Tu API está lista para ser probada en producción! 🚀
