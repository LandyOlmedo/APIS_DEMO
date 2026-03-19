import random
import time

import requests

URL = "https://iotdemos-default-rtdb.firebaseio.com/sensores/sucursal1.json"


def get_sensores() -> None:
    """Consulta el valor actual de los sensores en Firebase."""
    response = requests.get(URL, timeout=10)
    print(response.status_code)
    print(response.text)


def simular_sensores() -> None:
    """Envía nuevos valores cada 5 segundos."""
    while True:
        data = {
            "temperatura": random.randint(0, 100),
            "humedad": random.randint(0, 100),
        }
        response = requests.put(URL, json=data, timeout=10)
        print(response.status_code)
        print(response.text)
        time.sleep(3)


if __name__ == "__main__":
    simular_sensores()
