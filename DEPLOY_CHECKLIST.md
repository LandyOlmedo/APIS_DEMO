# Checklist de Despliegue en Render

## ✅ Requisitos completados

### Código y Configuración
- [x] API REST completa con 7 endpoints (GET, POST, PUT, DELETE)
- [x] Base de datos SQLite sincronizada con CSV
- [x] Validaciones de parámetros implementadas
- [x] Manejo de errores centralizado
- [x] 35 pruebas unitarias (100% pasadas)
- [x] Importaciones corregidas (sin errores de ImportError)

### Archivos de Configuración
- [x] `render.yaml` - Configuración de Render
- [x] `Procfile` - Comando de inicio
- [x] `requirements.txt` - Dependencias (pytest agregado)
- [x] `.gitignore` - Archivos a ignorar

### Documentación
- [x] `DEPLOY_RENDER.md` - Guía completa de despliegue
- [x] `API_SPECIFICATION.md` - Especificación de endpoints
- [x] `DEVELOPMENT_GUIDE.md` - Guía de desarrollo
- [x] `test_main.py` - Pruebas unitarias

---

## 🚀 Pasos para desplegar en Render

### PASO 1: Preparar el repositorio Git

```bash
cd /workspaces/Fast_API
git add .
git commit -m "API REST completa con endpoints CRUD, validaciones y pruebas"
git push origin main
```

### PASO 2: Ir a Render.com

1. Abre [https://render.com](https://render.com)
2. Inicia sesión con tu cuenta
3. Haz clic en **"+ New"** → **"Web Service"**

### PASO 3: Conectar repositorio GitHub

1. Selecciona **"Connect a GitHub repository"**
2. Busca y selecciona **`LandyOlmedo/APIS_DEMO`**
3. Autoriza el acceso si te lo pide

### PASO 4: Configurar el servicio Web

Completa el formulario con estos valores:

```
Name:                    fastapi-contactos-api
Environment:             Python 3
Build Command:           pip install -r requirements.txt
Start Command:           uvicorn apis.contactos.main:app --host 0.0.0.0 --port $PORT
Plan:                    Free
Region:                  Ohio (u otra)
Auto-Deploy:             Yes (recomendado)
```

### PASO 5: Desplegar

1. Haz clic en **"Create Web Service"**
2. Render comenzará la construcción
3. Espera a ver **"Live"** en verde (2-5 minutos)

---

## 📋 Verificación después del despliegue

### URL de acceso
Tu API estará en:
```
https://fastapi-contactos-api.onrender.com
```

### Pruebas rápidas

#### 1. Verificar que la API responde
```bash
curl https://fastapi-contactos-api.onrender.com/
```

#### 2. Listar contactos
```bash
curl "https://fastapi-contactos-api.onrender.com/v1/contactos?limit=5&skip=0"
```

#### 3. Obtener un contacto
```bash
curl https://fastapi-contactos-api.onrender.com/v1/contactos/1
```

#### 4. Crear un contacto
```bash
curl -X POST https://fastapi-contactos-api.onrender.com/v1/contacto \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Test","telefono":"1234567890","email":"test@test.com"}'
```

### Documentación interactiva
```
https://fastapi-contactos-api.onrender.com/docs
```

---

## 🔧 Soluciones rápidas

| Problema | Solución |
|----------|----------|
| **Build failed** | Revisa el log en Render. Verifica `requirements.txt` |
| **Application startup failed** | Revisa que `apis/contactos/main.py` exista |
| **404 on endpoint** | Asegúrate que la ruta sea `/v1/contactos` (con `/v1`) |
| **ImportError** | Ya está corregido. Las importaciones usan módulos absolutos |

---

## 📊 Resumen técnico

- **Framework**: FastAPI 0.128.2
- **Servidor**: Uvicorn 0.40.0
- **Base de datos**: SQLite (100 contactos del CSV)
- **Tests**: 35 pruebas pytest (100% pasadas)
- **Python**: 3.11+

---

## 💡 Tips importantes

### Plan Free de Render
- Se apaga después de 15 minutos sin actividad
- Se reinicia automáticamente en siguientes solicitudes
- Perfecto para desarrollo y pruebas

### Base de datos en Render
- SQLite se reinicia con cada deploy
- Para producción, considera:
  - PostgreSQL en Render
  - MongoDB Atlas
  - Firebase

### Dominios personalizados
Para usar tu dominio propio:
1. Ve a Settings en tu servicio Render
2. Agrega Custom Domain
3. Actualiza DNS settings en tu registrador

---

## ✨ Características de la API desplegada

✅ CRUD completo (Create, Read, Update, Delete)  
✅ Búsqueda flexible (por nombre o ID)  
✅ Paginación (limit y skip)  
✅ 100 contactos precargados  
✅ Validaciones de parámetros  
✅ Respuestas JSON consistentes  
✅ Documentación Swagger UI  
✅ 35 tests unitarios  

---

## 📞 Soporte

Si encuentras problemas:
1. Revisa los logs en el dashboard de Render
2. Verifica la [guía de despliegue](DEPLOY_RENDER.md)
3. Consulta [API_SPECIFICATION.md](apis/contactos/API_SPECIFICATION.md)
4. Ejecuta tests locales: `pytest test_main.py`

---

## 🎉 ¡Listo para desplegar!

Sigue los pasos anteriores y tu API estará disponible en minutos.
