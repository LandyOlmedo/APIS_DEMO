from fastapi import FastAPI, Query, Body
import sqlite3
import os
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Optional

# Ruta de la base de datos
DB_PATH = os.path.join(os.path.dirname(__file__), "agendadb.sqlite3")

app = FastAPI()

# Inicializar base de datos al startup
@app.on_event("startup")
async def startup_event():
    """Inicializa la base de datos al iniciar la aplicación"""
    try:
        # Intenta importar como si estuvieras en la raíz del proyecto (Render)
        from apis.contactos.init_db import init_database
    except ModuleNotFoundError:
        # Si no funciona, intenta importar como si estuvieras en el directorio actual (desarrollo local)
        from init_db import init_database
    init_database()


@app.get(
    "/",
    status_code=200,
    summary="Endpoint de raiz",
    description="Bienvenido a la API de agenda")
def get_root():
    data = {
        "message": "API de la Agenda",
        "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    return data


@app.get(
    "/v1/contactos",
    status_code=200,
    summary="Endpoint de contactos",
    description="""Endpoint que regresa los contactos paginados, 
    utiliza los siguientes query params:
    limit:int -> indica el numero de registros a regresar
    skip:int -> indica el numero de registros a omitir
    """,
    responses={
        200: {
            "description": "Respuesta exitosa con lista de contactos",
            "content": {
                "application/json": {
                    "example": {
                        "table": "contactos",
                        "items": [
                            {
                                "id_contacto": 1,
                                "nombre": "María Rodríguez",
                                "telefono": "0005550001",
                                "email": "contacto1@example.com"
                            },
                            {
                                "id_contacto": 2,
                                "nombre": "Pedro González",
                                "telefono": "0005550002",
                                "email": "contacto2@example.com"
                            }
                        ],
                        "count": 2,
                        "total": 100,
                        "datetime": "13/02/2026 10:30:15",
                        "message": "Datos consultados correctamente",
                        "limit": 10,
                        "skip": 0
                    }
                }
            }
        }
    }
)
async def get_contactos(
    limit: Optional[int] = Query(default=None, examples=[5], description="Número de registros a regresar"),
    skip: Optional[int] = Query(default=None, examples=[0], description="Número de registros a omitir")
):
    if limit is None and skip is None:
        return JSONResponse(
            status_code=400,
            content={
                "table": "contactos",
                "items": [],
                "count": 0,
                "total": 0,
                "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "message": "Debes enviar los parámetros 'limit' y 'skip'",
                "limit": limit,
                "skip": skip
            }
        )

    if limit is None:
        return JSONResponse(
            status_code=400,
            content={
                "table": "contactos",
                "items": [],
                "count": 0,
                "total": 0,
                "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "message": "El parámetro 'limit' es obligatorio",
                "limit": limit,
                "skip": skip
            }
        )

    if skip is None:
        return JSONResponse(
            status_code=400,
            content={
                "table": "contactos",
                "items": [],
                "count": 0,
                "total": 0,
                "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "message": "El parámetro 'skip' es obligatorio",
                "limit": limit,
                "skip": skip
            }
        )

    if limit == 0:
        return JSONResponse(
            status_code=400,
            content={
                "table": "contactos",
                "items": [],
                "count": 0,
                "total": 0,
                "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "message": "El parámetro 'limit' no puede ser 0",
                "limit": limit,
                "skip": skip
            }
        )
    
    if limit < 0 or skip < 0:
        return JSONResponse(
            status_code=400,
            content={
                "table": "contactos",
                "items": [],
                "count": 0,
                "total": 0,
                "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "message": "Los parámetros 'limit' y 'skip' no pueden ser negativos",
                "limit": limit,
                "skip": skip
            }
        )

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM contactos")
        total = cursor.fetchone()[0]
        
        cursor.execute(
            "SELECT id_contacto, nombre, telefono, email FROM contactos LIMIT ? OFFSET ?",
            (limit, skip)
        )
        rows = cursor.fetchall()
        
        contactos = []
        for row in rows:
            contactos.append({
                "id_contacto": row[0],
                "nombre": row[1],
                "telefono": row[2],
                "email": row[3]
            })
        
        conn.close()
        
        response = {
            "table": "contactos",
            "items": contactos,
            "count": len(contactos),
            "total": total,
            "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "message": "Datos consultados correctamente",
            "limit": limit,
            "skip": skip
        }
        return JSONResponse(
            status_code=200,
            content=response
        )
    
    except Exception as e:
        print(f"Error al consultar contactos: {e.args}")
        #raise HTTPException(status_code=400, detail="Error al consultar los contactos")
        return JSONResponse(
            status_code=400,
            content={
                "table": "contactos",
                "items": [],
                "count": 0,
                "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "message": "Error al consultar los contactos",
                "limit": limit, 
                "skip": skip
                }
            )


@app.get(
    "/v1/contactos/{id_contacto}",
    status_code=200,
    summary="Consultar un contacto por ID",
    description="Endpoint que regresa un contacto específico por su ID",
    responses={
        200: {
            "description": "Contacto encontrado exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "table": "contactos",
                        "item": {
                            "id_contacto": 1,
                            "nombre": "María Rodríguez",
                            "telefono": "0005550001",
                            "email": "contacto1@example.com"
                        },
                        "datetime": "16/02/2026 10:30:15",
                        "message": "Contacto encontrado correctamente"
                    }
                }
            }
        },
        400: {
            "description": "Contacto no encontrado",
            "content": {
                "application/json": {
                    "example": {
                        "table": "contactos",
                        "item": {},
                        "datetime": "16/02/2026 10:30:15",
                        "message": "El contacto no existe"
                    }
                }
            }
        }
    }
)
async def get_contacto(id_contacto: int):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id_contacto, nombre, telefono, email FROM contactos WHERE id_contacto = ?",
            (id_contacto,)
        )
        row = cursor.fetchone()
        conn.close()
        
        if row is None:
            return JSONResponse(
                status_code=400,
                content={
                    "table": "contactos",
                    "item": {},
                    "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "message": "El contacto no existe"
                }
            )
        
        contacto = {
            "id_contacto": row[0],
            "nombre": row[1],
            "telefono": row[2],
            "email": row[3]
        }
        
        return JSONResponse(
            status_code=200,
            content={
                "table": "contactos",
                "item": contacto,
                "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "message": "Contacto encontrado correctamente"
            }
        )
    
    except Exception as e:
        print(f"Error al consultar el contacto: {e.args}")
        return JSONResponse(
            status_code=400,
            content={
                "table": "contactos",
                "item": None,
                "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "message": "Error al consultar el contacto"
            }
        )


@app.get(
    "/v1/contacto",
    status_code=200,
    summary="Buscar un contacto por nombre o ID",
    description="Endpoint que busca un contacto por nombre o ID usando query params",
    responses={
        200: {
            "description": "Contacto encontrado exitosamente",
            "content": {
                "application/json": {
                    "example": {
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
                }
            }
        },
        400: {
            "description": "Parámetros inválidos o contacto no encontrado",
            "content": {
                "application/json": {
                    "example": {
                        "table": "contactos",
                        "item": {},
                        "datetime": "31/03/2026 10:30:15",
                        "message": "Debes enviar 'nombre' o 'id_contacto'"
                    }
                }
            }
        }
    }
)
async def buscar_contacto(
    nombre: Optional[str] = Query(default=None, description="Nombre del contacto"),
    id_contacto: Optional[int] = Query(default=None, description="ID del contacto")
):
    if nombre is None and id_contacto is None:
        return JSONResponse(
            status_code=400,
            content={
                "table": "contactos",
                "item": {},
                "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "message": "Debes enviar 'nombre' o 'id_contacto'"
            }
        )
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        if id_contacto is not None:
            cursor.execute(
                "SELECT id_contacto, nombre, telefono, email FROM contactos WHERE id_contacto = ?",
                (id_contacto,)
            )
        else:
            cursor.execute(
                "SELECT id_contacto, nombre, telefono, email FROM contactos WHERE nombre LIKE ?",
                (f"%{nombre}%",)
            )
        
        row = cursor.fetchone()
        conn.close()
        
        if row is None:
            return JSONResponse(
                status_code=400,
                content={
                    "table": "contactos",
                    "item": {},
                    "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "message": "El contacto no existe"
                }
            )
        
        contacto = {
            "id_contacto": row[0],
            "nombre": row[1],
            "telefono": row[2],
            "email": row[3]
        }
        
        return JSONResponse(
            status_code=200,
            content={
                "table": "contactos",
                "item": contacto,
                "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "message": "Contacto encontrado correctamente"
            }
        )
    
    except Exception as e:
        print(f"Error al buscar contacto: {e.args}")
        return JSONResponse(
            status_code=400,
            content={
                "table": "contactos",
                "item": {},
                "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "message": "Error al buscar el contacto"
            }
        )


@app.post(
    "/v1/contacto",
    status_code=201,
    summary="Crear un nuevo contacto",
    description="Endpoint para insertar un nuevo contacto con nombre, teléfono y email",
    responses={
        201: {
            "description": "Contacto creado exitosamente",
            "content": {
                "application/json": {
                    "example": {
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
                }
            }
        },
        400: {
            "description": "Error en los datos enviados",
            "content": {
                "application/json": {
                    "example": {
                        "table": "contactos",
                        "item": {},
                        "datetime": "31/03/2026 10:30:15",
                        "message": "Faltan campos requeridos o error en los datos"
                    }
                }
            }
        }
    }
)
async def crear_contacto(data: dict = Body(...)):
    if not all(key in data for key in ["nombre", "telefono", "email"]):
        return JSONResponse(
            status_code=400,
            content={
                "table": "contactos",
                "item": {},
                "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "message": "Faltan campos requeridos: nombre, telefono, email"
            }
        )
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO contactos (nombre, telefono, email) VALUES (?, ?, ?)",
            (data["nombre"], data["telefono"], data["email"])
        )
        
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        
        contacto = {
            "id_contacto": new_id,
            "nombre": data["nombre"],
            "telefono": data["telefono"],
            "email": data["email"]
        }
        
        return JSONResponse(
            status_code=201,
            content={
                "table": "contactos",
                "item": contacto,
                "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "message": "Contacto creado correctamente"
            }
        )
    
    except Exception as e:
        print(f"Error al crear contacto: {e.args}")
        return JSONResponse(
            status_code=400,
            content={
                "table": "contactos",
                "item": {},
                "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "message": "Error al crear el contacto"
            }
        )


@app.put(
    "/v1/contacto",
    status_code=200,
    summary="Modificar un contacto",
    description="Endpoint para actualizar los datos de un contacto existente por su ID",
    responses={
        200: {
            "description": "Contacto actualizado exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "table": "contactos",
                        "item": {
                            "id_contacto": 1,
                            "nombre": "Sophia Carey Actualizado",
                            "telefono": "1234567890",
                            "email": "nuevo@example.com"
                        },
                        "datetime": "31/03/2026 10:30:15",
                        "message": "Contacto actualizado correctamente"
                    }
                }
            }
        },
        400: {
            "description": "Error - Contacto no existe o datos inválidos",
            "content": {
                "application/json": {
                    "example": {
                        "table": "contactos",
                        "item": {},
                        "datetime": "31/03/2026 10:30:15",
                        "message": "El contacto no existe"
                    }
                }
            }
        }
    }
)
async def actualizar_contacto(data: dict = Body(...)):
    if "id_contacto" not in data:
        return JSONResponse(
            status_code=400,
            content={
                "table": "contactos",
                "item": {},
                "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "message": "El campo 'id_contacto' es obligatorio"
            }
        )
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Verificar que el contacto existe
        cursor.execute("SELECT * FROM contactos WHERE id_contacto = ?", (data["id_contacto"],))
        if cursor.fetchone() is None:
            conn.close()
            return JSONResponse(
                status_code=400,
                content={
                    "table": "contactos",
                    "item": {},
                    "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "message": "El contacto no existe"
                }
            )
        
        # Actualizar los campos proporcionados
        campos = []
        valores = []
        
        if "nombre" in data:
            campos.append("nombre = ?")
            valores.append(data["nombre"])
        if "telefono" in data:
            campos.append("telefono = ?")
            valores.append(data["telefono"])
        if "email" in data:
            campos.append("email = ?")
            valores.append(data["email"])
        
        if not campos:
            conn.close()
            return JSONResponse(
                status_code=400,
                content={
                    "table": "contactos",
                    "item": {},
                    "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "message": "Debes enviar al menos un campo a actualizar"
                }
            )
        
        valores.append(data["id_contacto"])
        query = f"UPDATE contactos SET {', '.join(campos)} WHERE id_contacto = ?"
        
        cursor.execute(query, valores)
        conn.commit()
        
        # Obtener el contacto actualizado
        cursor.execute(
            "SELECT id_contacto, nombre, telefono, email FROM contactos WHERE id_contacto = ?",
            (data["id_contacto"],)
        )
        row = cursor.fetchone()
        conn.close()
        
        contacto = {
            "id_contacto": row[0],
            "nombre": row[1],
            "telefono": row[2],
            "email": row[3]
        }
        
        return JSONResponse(
            status_code=200,
            content={
                "table": "contactos",
                "item": contacto,
                "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "message": "Contacto actualizado correctamente"
            }
        )
    
    except Exception as e:
        print(f"Error al actualizar contacto: {e.args}")
        return JSONResponse(
            status_code=400,
            content={
                "table": "contactos",
                "item": {},
                "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "message": "Error al actualizar el contacto"
            }
        )


@app.delete(
    "/v1/contacto",
    status_code=200,
    summary="Eliminar un contacto",
    description="Endpoint para eliminar un contacto por su ID",
    responses={
        200: {
            "description": "Contacto eliminado exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "table": "contactos",
                        "datetime": "31/03/2026 10:30:15",
                        "message": "Contacto eliminado correctamente"
                    }
                }
            }
        },
        400: {
            "description": "Error - Contacto no existe",
            "content": {
                "application/json": {
                    "example": {
                        "table": "contactos",
                        "datetime": "31/03/2026 10:30:15",
                        "message": "El contacto no existe"
                    }
                }
            }
        }
    }
)
async def eliminar_contacto(id_contacto: int = Query(..., description="ID del contacto a eliminar")):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Verificar que el contacto existe
        cursor.execute("SELECT * FROM contactos WHERE id_contacto = ?", (id_contacto,))
        if cursor.fetchone() is None:
            conn.close()
            return JSONResponse(
                status_code=400,
                content={
                    "table": "contactos",
                    "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "message": "El contacto no existe"
                }
            )
        
        cursor.execute("DELETE FROM contactos WHERE id_contacto = ?", (id_contacto,))
        conn.commit()
        conn.close()
        
        return JSONResponse(
            status_code=200,
            content={
                "table": "contactos",
                "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "message": "Contacto eliminado correctamente"
            }
        )
    
    except Exception as e:
        print(f"Error al eliminar contacto: {e.args}")
        return JSONResponse(
            status_code=400,
            content={
                "table": "contactos",
                "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "message": "Error al eliminar el contacto"
            }
        )

