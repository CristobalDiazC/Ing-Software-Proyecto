const API_BASE = "http://127.0.0.1:8000";

// Carga y muestra la lista de libros
async function cargarLibros(q = "") {
  const tbody = document.getElementById("tabla-libros-gestion");
  // 5 columnas: ID, Nombre, Stock Total, Precio, Acciones
  tbody.innerHTML = "<tr><td colspan='5'>Cargando...</td></tr>";

  let url = `${API_BASE}/libros/`;
  if (q) {
    // La API /libros/ sí soporta el filtro 'q' para nombre.
    url += `?q=${encodeURIComponent(q)}`;
  }

  try {
    const res = await fetch(url);
    if (!res.ok) {
      throw new Error("Error al obtener el catálogo de libros");
    }

    const libros = await res.json();
    tbody.innerHTML = "";

    if (!libros.length) {
      tbody.innerHTML = "<tr><td colspan='5'>No hay libros registrados</td></tr>";
      return;
    }

    libros.forEach((libro) => {
      // ⚠️ NOTA: El stock total no es devuelto por el endpoint /libros/, 
      // así que usamos un valor de ejemplo. Se requiere modificar el backend
      // o hacer otra llamada a /inventario/ para obtener el stock real.
      const stockTotalEjemplo = Math.floor(Math.random() * 50) + 1;

      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${libro.id_libro}</td>
        <td>${libro.nombre}</td>
        <td>${stockTotalEjemplo}</td> 
        <td>${libro.precio != null ? "$" + libro.precio : "—"}</td>
        <td>
          <a class="link" href="#" onclick="alert('Editar libro ${libro.id_libro}')">Editar</a>
          <a class="link" href="#" onclick="eliminarLibro(${libro.id_libro}); return false;">Eliminar</a>
        </td>
      `;
      tbody.appendChild(tr);
    });
  } catch (e) {
    console.error(e);
    tbody.innerHTML = "<tr><td colspan='5'>Error al cargar libros</td></tr>";
  }
}

// Función para manejar la eliminación de un libro
window.eliminarLibro = async function (libroId) {
    if (!confirm(`¿Estás seguro de que quieres eliminar el libro ID: ${libroId}? Esto también eliminará su inventario asociado.`)) {
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/libros/${libroId}`, {
            method: "DELETE"
        });

        if (res.status === 204) {
            alert("✅ Libro eliminado correctamente.");
            cargarLibros(); // Recargar lista
        } else {
            const data = await res.json();
            alert("❌ Error al eliminar: " + (data.detail || "Error desconocido."));
        }
    } catch (error) {
        console.error(error);
        alert("⚠️ Error al conectar con el servidor.");
    }
}


// Cuando carga la página
document.addEventListener("DOMContentLoaded", () => {
  // Cargar libros inicial
  cargarLibros();

  // Listener para el formulario de filtro/búsqueda
  const formFiltro = document.getElementById("filterFormLibros");

  if (formFiltro) {
    formFiltro.addEventListener("submit", function (e) {
      e.preventDefault();
      const q = this.q.value.trim();
      cargarLibros(q);
    });
  }
});