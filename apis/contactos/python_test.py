import sqlite3
from datetime import datetime
from pathlib import Path

import requests

URL_BASE = "http://localhost:8000"
DB_PATH = Path(__file__).with_name("agendadb.sqlite3")


def _assert_timestamp_format(value: str) -> None:
    """Ensure the API timestamp uses the expected day-first format."""
    datetime.strptime(value, "%d/%m/%Y %H:%M:%S")


def _get_expected_contact_window(limit: int, skip: int):
    """Read the SQLite DB to build the expected slice of contactos."""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM contactos")
    total = cursor.fetchone()[0]
    cursor.execute(
        "SELECT id_contacto, nombre, telefono, email FROM contactos LIMIT ? OFFSET ?",
        (limit, skip),
    )
    rows = cursor.fetchall()
    conn.close()

    items = [
        {"id_contacto": row[0], "nombre": row[1], "telefono": row[2], "email": row[3]}
        for row in rows
    ]
    return items, total


def _get_expected_contact_by_id(id_contacto: int):
    """Read the SQLite DB to get one contacto by ID."""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id_contacto, nombre, telefono, email FROM contactos WHERE id_contacto = ?",
        (id_contacto,),
    )
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    return {
        "id_contacto": row[0],
        "nombre": row[1],
        "telefono": row[2],
        "email": row[3],
    }


def test_read_root():
    response = requests.get(f"{URL_BASE}/")
    assert response.status_code == 200

    payload = response.json()
    assert payload["message"] == "API de la Agenda"
    assert set(payload.keys()) == {"message", "datetime"}
    _assert_timestamp_format(payload["datetime"])


def test_get_contactos_limit_10_skip_0():
    limit, skip = 10, 0
    response = requests.get(f"{URL_BASE}/v1/contactos", params={"limit": limit, "skip": skip})
    assert response.status_code == 200

    payload = response.json()
    expected_items, total = _get_expected_contact_window(limit, skip)
    assert payload["table"] == "contactos"
    assert payload["items"] == expected_items
    assert payload["count"] == len(expected_items)
    assert payload["total"] == total
    assert payload["message"] == "Datos consultados correctamente"
    assert payload["limit"] == limit
    assert payload["skip"] == skip
    _assert_timestamp_format(payload["datetime"])


def test_get_contactos_limit_10_skip_90():
    limit, skip = 10, 90
    response = requests.get(f"{URL_BASE}/v1/contactos", params={"limit": limit, "skip": skip})
    assert response.status_code == 200

    payload = response.json()
    expected_items, total = _get_expected_contact_window(limit, skip)
    assert payload["items"] == expected_items
    assert payload["count"] == len(expected_items)
    assert payload["total"] == total
    assert payload["limit"] == limit
    assert payload["skip"] == skip
    _assert_timestamp_format(payload["datetime"])


def test_get_contactos_limit_negativo_skip_0():
    response = requests.get(f"{URL_BASE}/v1/contactos", params={"limit": -10, "skip": 0})
    assert response.status_code == 400

    payload = response.json()
    assert payload["message"] == "Los parámetros 'limit' y 'skip' no pueden ser negativos"
    assert payload["items"] == []
    assert payload["count"] == 0
    assert payload["total"] == 0
    assert payload["limit"] == -10
    assert payload["skip"] == 0


def test_get_contactos_limit_10_skip_negativo():
    response = requests.get(f"{URL_BASE}/v1/contactos", params={"limit": 10, "skip": -10})
    assert response.status_code == 400

    payload = response.json()
    assert payload["message"] == "Los parámetros 'limit' y 'skip' no pueden ser negativos"
    assert payload["items"] == []
    assert payload["count"] == 0
    assert payload["total"] == 0
    assert payload["limit"] == 10
    assert payload["skip"] == -10


def test_get_contactos_limit_0_skip_0():
    response = requests.get(f"{URL_BASE}/v1/contactos", params={"limit": 0, "skip": 0})
    assert response.status_code == 400

    payload = response.json()
    assert payload["message"] == "El parámetro 'limit' no puede ser 0"
    assert payload["items"] == []
    assert payload["count"] == 0
    assert payload["total"] == 0
    assert payload["limit"] == 0
    assert payload["skip"] == 0


def test_get_contactos_skip_0():
    skip = 0
    response = requests.get(f"{URL_BASE}/v1/contactos", params={"skip": skip})
    assert response.status_code == 400

    payload = response.json()
    assert payload["message"] == "El parámetro 'limit' es obligatorio"
    assert payload["items"] == []
    assert payload["count"] == 0
    assert payload["total"] == 0
    assert payload["limit"] is None
    assert payload["skip"] == skip


def test_get_contactos_limit_10():
    limit = 10
    response = requests.get(f"{URL_BASE}/v1/contactos", params={"limit": limit})
    assert response.status_code == 400

    payload = response.json()
    assert payload["message"] == "El parámetro 'skip' es obligatorio"
    assert payload["items"] == []
    assert payload["count"] == 0
    assert payload["total"] == 0
    assert payload["limit"] == limit
    assert payload["skip"] is None


def test_get_contactos():
    response = requests.get(f"{URL_BASE}/v1/contactos")
    assert response.status_code == 400

    payload = response.json()
    assert payload["message"] == "Debes enviar los parámetros 'limit' y 'skip'"
    assert payload["items"] == []
    assert payload["count"] == 0
    assert payload["total"] == 0
    assert payload["limit"] is None
    assert payload["skip"] is None


def test_get_contactos_limit_x_skip_100():
    response = requests.get(f"{URL_BASE}/v1/contactos", params={"limit": "x", "skip": 100})
    assert response.status_code == 422

    payload = response.json()
    assert payload["detail"][0]["loc"][-1] == "limit"
    assert payload["detail"][0]["msg"].startswith("Input should be a valid integer")


def test_get_contactos_limit_10_skip_x():
    response = requests.get(f"{URL_BASE}/v1/contactos", params={"limit": 10, "skip": "x"})
    assert response.status_code == 422

    payload = response.json()
    assert payload["detail"][0]["loc"][-1] == "skip"
    assert payload["detail"][0]["msg"].startswith("Input should be a valid integer")


def test_get_contacto_by_id_existente():
    id_contacto = 1
    response = requests.get(f"{URL_BASE}/v1/contactos/{id_contacto}")
    assert response.status_code == 200

    payload = response.json()
    expected_item = _get_expected_contact_by_id(id_contacto)
    assert payload["table"] == "contactos"
    assert payload["item"] == expected_item
    assert payload["message"] == "Contacto encontrado correctamente"
    _assert_timestamp_format(payload["datetime"])


def test_get_contacto_by_id_no_existente():
    id_contacto = 99999
    response = requests.get(f"{URL_BASE}/v1/contactos/{id_contacto}")
    assert response.status_code == 400

    payload = response.json()
    assert payload["table"] == "contactos"
    assert payload["item"] == {}
    assert payload["message"] == "El contacto no existe"
    _assert_timestamp_format(payload["datetime"])


def test_get_contacto_by_id_negativo():
    id_contacto = -1
    response = requests.get(f"{URL_BASE}/v1/contactos/{id_contacto}")
    assert response.status_code == 400

    payload = response.json()
    assert payload["table"] == "contactos"
    assert payload["item"] == {}
    assert payload["message"] == "El contacto no existe"
    _assert_timestamp_format(payload["datetime"])


def test_get_contacto_by_id_invalido():
    response = requests.get(f"{URL_BASE}/v1/contactos/x")
    assert response.status_code == 422

    payload = response.json()
    assert payload["detail"][0]["loc"][-1] == "id_contacto"
    assert payload["detail"][0]["msg"].startswith("Input should be a valid integer")