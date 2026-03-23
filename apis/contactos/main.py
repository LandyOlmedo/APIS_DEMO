from fastapi import FastAPI, Query
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

