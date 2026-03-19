function getDatos() {
  const url = "https://iotdemos-default-rtdb.firebaseio.com/sensores/sucursal1.json";
  const sensores = new EventSource(url);

  sensores.addEventListener("put", function (e) {
    const json = JSON.parse(e.data);
    if (!json.data) return;

    for (const key in json.data) {
      const el = document.getElementById(key);
      if (el) {
        el.textContent = json.data[key];
      }
    }
  });

  sensores.onerror = function (err) {
    console.error("Error en EventSource:", err);
  };
}
