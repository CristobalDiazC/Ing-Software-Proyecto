const API_BASE = "http://127.0.0.1:8000";

// Carga y muestra la lista de usuarios
async function cargarUsuarios(q = "") {
  const tbody = document.getElementById("tabla-usuarios");
  // 6 columnas: ID, Nombre, Email, Rol, Punto de Venta ID, Acciones
  tbody.innerHTML = "<tr><td colspan='6'>Cargando...</td></tr>";

  let url = `${API_BASE}/usuarios/`;
  if (q) {
    // La API /usuarios/ sí soporta el filtro 'q' para nombre o email.
    url += `?q=${encodeURIComponent(q)}`;
  }

  try {
    const res = await fetch(url);
    if (!res.ok) {
      throw new Error("Error al obtener la lista de usuarios");
    }

    const usuarios = await res.json();
    tbody.innerHTML = "";

    if (!usuarios.length) {
      tbody.innerHTML = "<tr><td colspan='6'>No hay usuarios registrados</td></tr>";
      return;
    }

    usuarios.forEach((user) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${user.id_usuario}</td>
        <td>${user.nombre}</td>
        <td>${user.email || "—"}</td>
        <td>${user.rol}</td>
        <td>${user.punto_venta_id || "Global"}</td>
        <td>
          <a class="link" href="#" onclick="alert('Editar usuario ${user.id_usuario}')">Editar</a>
          <a class="link" href="#" onclick="eliminarUsuario(${user.id_usuario}); return false;">Eliminar</a>
        </td>
      `;
      tbody.appendChild(tr);
    });
  } catch (e) {
    console.error(e);
    tbody.innerHTML = "<tr><td colspan='6'>Error al cargar usuarios</td></tr>";
  }
}

// Función para manejar la eliminación de un usuario
window.eliminarUsuario = async function (usuarioId) {
    if (!confirm(`¿Estás seguro de que quieres eliminar el usuario ID: ${usuarioId}?`)) {
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/usuarios/${usuarioId}`, {
            method: "DELETE"
        });

        if (res.status === 204) {
            alert("✅ Usuario eliminado correctamente.");
            cargarUsuarios(); // Recargar lista
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
  // Cargar usuarios inicial
  cargarUsuarios();

  // Listener para el formulario de filtro/búsqueda
  const formFiltro = document.getElementById("filterFormUsuarios");

  if (formFiltro) {
    formFiltro.addEventListener("submit", function (e) {
      e.preventDefault();
      const q = this.q.value.trim();
      cargarUsuarios(q);
    });
  }
});