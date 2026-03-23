# Guía de Despliegue en Render

Esta guía te ayudará a desplegar tu API FastAPI en Render.

## Requisitos previos

1. ✅ Repositorio en GitHub (ya configurado)
2. ✅ Cuenta en [https://render.com](https://render.com)
3. ✅ Archivos de configuración listos:
   - `render.yaml` ✅
   - `Procfile` ✅
   - `requirements.txt` ✅

## Pasos para desplegar

### 1. Conectar GitHub a Render

1. Ve a [https://render.com](https://render.com)
2. Haz clic en **"New +"** → **"Web Service"**
3. Selecciona **"Connect a GitHub repository"**
4. Autoriza Render para acceder a tu GitHub
5. Busca y selecciona el repositorio `APIS_DEMO`

### 2. Configurar el servicio

En el formulario de creación del Web Service, configura:

| Parámetro | Valor |
|-----------|-------|
| **Name** | `fastapi-agenda` (o tu preferencia) |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn apis.contactos.main:app --host 0.0.0.0 --port $PORT` |
| **Plan** | `Free` (para desarrollo/pruebas) |
| **Region** | `Ohio` o la más cercana |

### 3. Variables de entorno (opcional)

Si necesitas variables de entorno, agrégalas en la sección **"Environment"**:
- Copia las variables desde `.env.example`
- Configura `DEBUG=False` para producción

### 4. Desplegar

1. Haz clic en **"Create Web Service"**
2. Render comenzará a construir y desplegar la aplicación
3. Espera a que el estado cambie a **"Live"** (puede tardar 2-3 minutos)

## URL de la API

Una vez desplegada, tu API estará disponible en:

```
https://fastapi-agenda.onrender.com
```

## Endpoints disponibles

### 1. Raíz
```bash
GET https://fastapi-agenda.onrender.com/
```

Respuesta:
```json
{
  "message": "API de la Agenda",
  "datetime": "23/03/2026 10:30:15"
}
```

### 2. Listar contactos
```bash
GET https://fastapi-agenda.onrender.com/v1/contactos?limit=10&skip=0
```

Parámetros requeridos:
- `limit`: número de registros a retornar
- `skip`: número de registros a saltar

### 3. Obtener contacto por ID
```bash
GET https://fastapi-agenda.onrender.com/v1/contactos/{id}
```

## Ejemplo con cURL

```bash
# Obtener primeros 10 contactos
curl "https://fastapi-agenda.onrender.com/v1/contactos?limit=10&skip=0"

# Obtener un contacto específico
curl "https://fastapi-agenda.onrender.com/v1/contactos/1"
```

## Documentación interactiva

Render proporciona acceso a Swagger UI:

```
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
