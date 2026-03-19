import os
import requests
import web

urls = (
    '/', 'GetSensores',
    '/led', 'GetLed'
)

TEMPLATES_DIR = os.path.dirname(__file__)
render = web.template.render(TEMPLATES_DIR)
app = web.application(urls, globals())


class GetSensores:
    def GET(self):

        url_distance = "https://iot2026-11c9d-default-rtdb.firebaseio.com/distance.json"
        response_distance = requests.get(url_distance)
        data = response_distance.json()

        url_led = "https://iot2026-11c9d-default-rtdb.firebaseio.com/led/status.json"
        response_led = requests.get(url_led)
        estado = response_led.json()

        return render.index(data, estado)


    def POST(self):

        data = web.input()

        nuevo_estado = data.estado

        if nuevo_estado == "true":
            nuevo_estado = True
        else:
            nuevo_estado = False

        url = "https://iot2026-11c9d-default-rtdb.firebaseio.com/led/status.json"

        requests.put(
            url,
            json=nuevo_estado,
            headers={"Content-Type":"application/json"}
        )

        raise web.seeother('/')


if __name__ == "__main__":
    web.httpserver.runsimple(app.wsgifunc(), ("0.0.0.0", 8090))