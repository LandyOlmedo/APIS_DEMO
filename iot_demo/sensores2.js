async function getDatos() {
  const url = "https://iotdemos-default-rtdb.firebaseio.com/sensores/sucursal1.json";

  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error("Error al obtener datos");

    const json = await response.json();
    if (!json) return;

    for (const key in json) {
      const el = document.getElementById(key);
      if (el) {
        el.textContent = json[key];
      }
    }
  } catch (error) {
    console.error("Error en la peticion:", error.message);
  }
}

setInterval(getDatos, 5000);
