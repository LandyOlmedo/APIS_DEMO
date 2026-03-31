import pytest
import json
import sqlite3
import os
from fastapi.testclient import TestClient
from main import app
from datetime import datetime

# Cliente de prueba para FastAPI
client = TestClient(app)

# Ruta de la base de datos de prueba
DB_PATH = os.path.join(os.path.dirname(__file__), "agendadb.sqlite3")


class TestRootEndpoint:
    """Pruebas del endpoint raíz GET /"""
    
    def test_get_root_success(self):
        """Test: GET / regresa mensaje de bienvenida"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["message"] == "API de la Agenda"
        assert "datetime" in data
    
    def test_get_root_has_datetime(self):
        """Test: GET / incluye datetime"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "datetime" in data
        # Validar formato de fecha
        datetime.strptime(data["datetime"], "%d/%m/%Y %H:%M:%S")


class TestGetContactosEndpoint:
    """Pruebas del endpoint GET /v1/contactos"""
    
    def test_get_contactos_without_params(self):
        """Test: GET /v1/contactos sin parámetros regresa error 400"""
        response = client.get("/v1/contactos")
        assert response.status_code == 400
        data = response.json()
        assert data["message"] == "Debes enviar los parámetros 'limit' y 'skip'"
    
    def test_get_contactos_without_limit(self):
        """Test: GET /v1/contactos sin limit regresa error 400"""
        response = client.get("/v1/contactos?skip=0")
        assert response.status_code == 400
        data = response.json()
        assert "limit" in data["message"].lower()
    
    def test_get_contactos_without_skip(self):
        """Test: GET /v1/contactos sin skip regresa error 400"""
        response = client.get("/v1/contactos?limit=5")
        assert response.status_code == 400
        data = response.json()
        assert "skip" in data["message"].lower()
    
    def test_get_contactos_with_zero_limit(self):
        """Test: GET /v1/contactos con limit=0 regresa error 400"""
        response = client.get("/v1/contactos?limit=0&skip=0")
        assert response.status_code == 400
        data = response.json()
        assert "limit" in data["message"].lower() and "0" in data["message"]
    
    def test_get_contactos_with_negative_params(self):
        """Test: GET /v1/contactos con parámetros negativos regresa error 400"""
        response = client.get("/v1/contactos?limit=-5&skip=0")
        assert response.status_code == 400
        data = response.json()
        assert "negativos" in data["message"].lower()
    
    def test_get_contactos_success(self):
        """Test: GET /v1/contactos con parámetros válidos regresa 200"""
        response = client.get("/v1/contactos?limit=5&skip=0")
        assert response.status_code == 200
        data = response.json()
        assert data["table"] == "contactos"
        assert "items" in data
        assert "count" in data
        assert "total" in data
        assert "datetime" in data
        assert "message" in data
        assert data["limit"] == 5
        assert data["skip"] == 0
    
    def test_get_contactos_pagination(self):
        """Test: GET /v1/contactos respeta parámetros de paginación"""
        response = client.get("/v1/contactos?limit=10&skip=5")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) <= 10
        assert data["limit"] == 10
        assert data["skip"] == 5
    
    def test_get_contactos_returns_valid_format(self):
        """Test: GET /v1/contactos regresa contactos con formato válido"""
        response = client.get("/v1/contactos?limit=1&skip=0")
        assert response.status_code == 200
        data = response.json()
        if len(data["items"]) > 0:
            contacto = data["items"][0]
            assert "id_contacto" in contacto
            assert "nombre" in contacto
            assert "telefono" in contacto
            assert "email" in contacto


class TestGetContactoByIdEndpoint:
    """Pruebas del endpoint GET /v1/contactos/{id_contacto}"""
    
    def test_get_contacto_by_id_success(self):
        """Test: GET /v1/contactos/1 regresa un contacto existente"""
        response = client.get("/v1/contactos/1")
        assert response.status_code == 200
        data = response.json()
        assert data["table"] == "contactos"
        assert "item" in data
        assert data["item"]["id_contacto"] == 1
        assert "nombre" in data["item"]
        assert "telefono" in data["item"]
        assert "email" in data["item"]
    
    def test_get_contacto_by_id_not_found(self):
        """Test: GET /v1/contactos/99999 regresa error 400 para ID inexistente"""
        response = client.get("/v1/contactos/99999")
        assert response.status_code == 400
        data = response.json()
        assert "no existe" in data["message"].lower()
    
    def test_get_contacto_by_id_format(self):
        """Test: GET /v1/contactos/{id} regresa formato válido"""
        response = client.get("/v1/contactos/1")
        assert response.status_code == 200
        data = response.json()
        assert data["table"] == "contactos"
        assert "datetime" in data
        assert "message" in data


class TestBuscarContactoEndpoint:
    """Pruebas del endpoint GET /v1/contacto (búsqueda)"""
    
    def test_buscar_contacto_without_params(self):
        """Test: GET /v1/contacto sin parámetros regresa error 400"""
        response = client.get("/v1/contacto")
        assert response.status_code == 400
        data = response.json()
        assert "nombre" in data["message"].lower() or "id_contacto" in data["message"].lower()
    
    def test_buscar_contacto_by_id(self):
        """Test: GET /v1/contacto?id_contacto=1 busca por ID"""
        response = client.get("/v1/contacto?id_contacto=1")
        assert response.status_code == 200
        data = response.json()
        assert data["item"]["id_contacto"] == 1
    
    def test_buscar_contacto_by_nombre(self):
        """Test: GET /v1/contacto?nombre=Sophia busca por nombre"""
        response = client.get("/v1/contacto?nombre=Sophia")
        assert response.status_code == 200
        data = response.json()
        assert "Sophia" in data["item"]["nombre"]
    
    def test_buscar_contacto_nombre_no_encontrado(self):
        """Test: GET /v1/contacto con nombre inexistente regresa error 400"""
        response = client.get("/v1/contacto?nombre=NOMBRE_INEXISTENTE_XYZ")
        assert response.status_code == 400
        data = response.json()
        assert "no existe" in data["message"].lower()
    
    def test_buscar_contacto_id_no_encontrado(self):
        """Test: GET /v1/contacto con ID inexistente regresa error 400"""
        response = client.get("/v1/contacto?id_contacto=99999")
        assert response.status_code == 400
        data = response.json()
        assert "no existe" in data["message"].lower()


class TestCrearContactoEndpoint:
    """Pruebas del endpoint POST /v1/contacto"""
    
    def test_crear_contacto_success(self):
        """Test: POST /v1/contacto crea un nuevo contacto"""
        nuevo_contacto = {
            "nombre": "Test Usuario",
            "telefono": "5551234567",
            "email": "test@example.com"
        }
        response = client.post("/v1/contacto", data=nuevo_contacto)
        assert response.status_code == 201
        data = response.json()
        assert data["table"] == "contactos"
        assert data["item"]["nombre"] == "Test Usuario"
        assert data["item"]["telefono"] == "5551234567"
        assert data["item"]["email"] == "test@example.com"
        assert "id_contacto" in data["item"]
    
    def test_crear_contacto_sin_nombre(self):
        """Test: POST /v1/contacto sin nombre regresa error 422 (validación)"""
        contacto_incompleto = {
            "telefono": "5551234567",
            "email": "test@example.com"
        }
        response = client.post("/v1/contacto", data=contacto_incompleto)
        assert response.status_code == 422  # Pydantic devuelve 422 para errores de validación
    
    def test_crear_contacto_sin_telefono(self):
        """Test: POST /v1/contacto sin teléfono regresa error 422 (validación)"""
        contacto_incompleto = {
            "nombre": "Test",
            "email": "test@example.com"
        }
        response = client.post("/v1/contacto", data=contacto_incompleto)
        assert response.status_code == 422
    
    def test_crear_contacto_sin_email(self):
        """Test: POST /v1/contacto sin email regresa error 422 (validación)"""
        contacto_incompleto = {
            "nombre": "Test",
            "telefono": "5551234567"
        }
        response = client.post("/v1/contacto", data=contacto_incompleto)
        assert response.status_code == 422
    
    def test_crear_contacto_campos_vacios(self):
        """Test: POST /v1/contacto con campos vacíos"""
        contacto = {
            "nombre": "",
            "telefono": "",
            "email": ""
        }
        response = client.post("/v1/contacto", data=contacto)
        # Campos vacíos fallan validación de min_length
        assert response.status_code == 422


class TestActualizarContactoEndpoint:
    """Pruebas del endpoint PUT /v1/contacto"""
    
    def test_actualizar_contacto_success(self):
        """Test: PUT /v1/contacto actualiza un contacto existente"""
        # Primero crear un contacto
        nuevo = {
            "nombre": "Test Update",
            "telefono": "5559999999",
            "email": "update@example.com"
        }
        create_response = client.post("/v1/contacto", data=nuevo)
        contacto_id = create_response.json()["item"]["id_contacto"]
        
        # Luego actualizarlo
        actualizar = {
            "id_contacto": contacto_id,
            "nombre": "Test Actualizado",
            "email": "actualizado@example.com"
        }
        response = client.put("/v1/contacto", data=actualizar)
        assert response.status_code == 200
        data = response.json()
        assert data["item"]["nombre"] == "Test Actualizado"
        assert data["item"]["email"] == "actualizado@example.com"
    
    def test_actualizar_contacto_sin_id(self):
        """Test: PUT /v1/contacto sin id_contacto regresa error 400"""
        actualizar = {
            "nombre": "Test",
            "email": "test@example.com"
        }
        response = client.put("/v1/contacto", data=actualizar)
        assert response.status_code == 422  # Pydantic valida que id_contacto es requerido

    
    def test_actualizar_contacto_id_no_existe(self):
        """Test: PUT /v1/contacto con ID inexistente regresa error 400"""
        actualizar = {
            "id_contacto": 99999,
            "nombre": "Test"
        }
        response = client.put("/v1/contacto", data=actualizar)
        assert response.status_code == 400
        data = response.json()
        assert "no existe" in data["message"].lower()
    
    def test_actualizar_contacto_sin_campos(self):
        """Test: PUT /v1/contacto con solo id_contacto regresa error 400"""
        actualizar = {
            "id_contacto": 1
        }
        response = client.put("/v1/contacto", data=actualizar)
        assert response.status_code == 400
        data = response.json()
        assert "campo" in data["message"].lower()
    
    def test_actualizar_contacto_solo_nombre(self):
        """Test: PUT /v1/contacto actualiza solo el nombre"""
        # Crear contacto
        nuevo = {
            "nombre": "Test Solo Nombre",
            "telefono": "5558888888",
            "email": "solo@example.com"
        }
        create_response = client.post("/v1/contacto", data=nuevo)
        contacto_id = create_response.json()["item"]["id_contacto"]
        
        # Actualizar solo nombre
        actualizar = {
            "id_contacto": contacto_id,
            "nombre": "Nombre Actualizado"
        }
        response = client.put("/v1/contacto", data=actualizar)
        assert response.status_code == 200
        data = response.json()
        assert data["item"]["nombre"] == "Nombre Actualizado"


class TestEliminarContactoEndpoint:
    """Pruebas del endpoint DELETE /v1/contacto"""
    
    def test_eliminar_contacto_success(self):
        """Test: DELETE /v1/contacto elimina un contacto existente"""
        # Crear un contacto
        nuevo = {
            "nombre": "Test Eliminar",
            "telefono": "5557777777",
            "email": "eliminar@example.com"
        }
        create_response = client.post("/v1/contacto", data=nuevo)
        contacto_id = create_response.json()["item"]["id_contacto"]
        
        # Eliminarlo
        response = client.delete(f"/v1/contacto?id_contacto={contacto_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["table"] == "contactos"
        assert "eliminado" in data["message"].lower()
    
    def test_eliminar_contacto_no_existe(self):
        """Test: DELETE /v1/contacto con ID inexistente regresa error 400"""
        response = client.delete("/v1/contacto?id_contacto=99999")
        assert response.status_code == 400
        data = response.json()
        assert "no existe" in data["message"].lower()
    
    def test_eliminar_contacto_sin_id(self):
        """Test: DELETE /v1/contacto sin id_contacto regresa error"""
        response = client.delete("/v1/contacto")
        assert response.status_code in [400, 422]  # 422 si FastAPI valida query params
    
    def test_eliminar_contacto_verificar_no_existe(self):
        """Test: Verifica que contacto eliminado no existe después"""
        # Crear contacto
        nuevo = {
            "nombre": "Test Verificar Eliminar",
            "telefono": "5556666666",
            "email": "verif@example.com"
        }
        create_response = client.post("/v1/contacto", data=nuevo)
        contacto_id = create_response.json()["item"]["id_contacto"]
        
        # Eliminar
        delete_response = client.delete(f"/v1/contacto?id_contacto={contacto_id}")
        assert delete_response.status_code == 200
        
        # Intentar obtener el contacto eliminado
        get_response = client.get(f"/v1/contactos/{contacto_id}")
        assert get_response.status_code == 400
        assert "no existe" in get_response.json()["message"].lower()


class TestIntegracion:
    """Pruebas de integración entre endpoints"""
    
    def test_flujo_completo(self):
        """Test: Flujo completo de CRUD"""
        # CREATE
        nuevo_contacto = {
            "nombre": "Juan Prueba",
            "telefono": "5551111111",
            "email": "juan@test.com"
        }
        create_response = client.post("/v1/contacto", data=nuevo_contacto)
        assert create_response.status_code == 201
        contacto_id = create_response.json()["item"]["id_contacto"]
        
        # READ por ID
        read_response = client.get(f"/v1/contactos/{contacto_id}")
        assert read_response.status_code == 200
        assert read_response.json()["item"]["nombre"] == "Juan Prueba"
        
        # UPDATE
        actualizar = {
            "id_contacto": contacto_id,
            "nombre": "Juan Prueba Actualizado"
        }
        update_response = client.put("/v1/contacto", data=actualizar)
        assert update_response.status_code == 200
        assert update_response.json()["item"]["nombre"] == "Juan Prueba Actualizado"
        
        # DELETE
        delete_response = client.delete(f"/v1/contacto?id_contacto={contacto_id}")
        assert delete_response.status_code == 200
    
    def test_busqueda_despues_creacion(self):
        """Test: Búsqueda funciona inmediatamente después de crear"""
        nuevo_contacto = {
            "nombre": "Carlos Búsqueda",
            "telefono": "5552222222",
            "email": "carlos@test.com"
        }
        create_response = client.post("/v1/contacto", data=nuevo_contacto)
        assert create_response.status_code == 201
        
        # Buscar por nombre
        search_response = client.get("/v1/contacto?nombre=Carlos")
        assert search_response.status_code == 200
        assert "Carlos" in search_response.json()["item"]["nombre"]
    
    def test_paginacion_respeta_total(self):
        """Test: Total de registros es consistente en paginación"""
        # Primera consulta
        response1 = client.get("/v1/contactos?limit=5&skip=0")
        total1 = response1.json()["total"]
        
        # Segunda consulta con diferentes parámetros
        response2 = client.get("/v1/contactos?limit=10&skip=0")
        total2 = response2.json()["total"]
        
        # El total debe ser el mismo
        assert total1 == total2
