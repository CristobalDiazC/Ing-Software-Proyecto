const API_BASE = "http://127.0.0.1:8000";

async function cargarActividadReciente() {
  const ul = document.getElementById("actividad-list");
  if (!ul) return;

  ul.innerHTML = "<li class='muted'>Cargando actividad...</li>";

  try {
    // Pedimos todos los movimientos ordenados del más nuevo al más viejo
    const res = await fetch(`${API_BASE}/movimientos/`);
    const movimientos = await res.json();

    if (!Array.isArray(movimientos) || movimientos.length === 0) {
      ul.innerHTML = "<li class='muted'>No hay movimientos recientes.</li>";
      return;
    }

    // Nos quedamos solo con los 5 más recientes
    const recientes = movimientos.slice(0, 5);

    ul.innerHTML = "";

    recientes.forEach(mov => {
      const fecha = new Date(mov.fecha_movimiento);
      const fechaTexto = fecha.toLocaleString("es-CL", {
        dateStyle: "short",
        timeStyle: "short"
      });

      let tipoTexto = "";
      if (mov.tipo === "venta") tipoTexto = "Venta";
      else if (mov.tipo === "entrada") tipoTexto = "Ingreso";
      else if (mov.tipo === "salida") tipoTexto = "Salida";
      else if (mov.tipo === "ajuste") tipoTexto = "Ajuste";
      else tipoTexto = mov.tipo;

      const li = document.createElement("li");
      li.textContent = `${tipoTexto} — Cant: ${mov.cantidad} — ${fechaTexto}`;
      ul.appendChild(li);
    });
  } catch (err) {
    console.error(err);
    ul.innerHTML = "<li class='muted'>Error al cargar la actividad.</li>";
  }
}

// Cuando se cargue la página, pedimos la actividad
window.addEventListener("DOMContentLoaded", cargarActividadReciente);
