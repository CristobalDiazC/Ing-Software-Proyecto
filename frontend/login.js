document.getElementById("loginForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const email = document.querySelector("input[name='email']").value;
  const password = document.querySelector("input[name='password']").value;

  try {
    const response = await fetch("http://127.0.0.1:5000/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    if (response.ok) {
      // Mostrar mensaje
      alert("✅ " + data.message);

      // 🔹 Guardar el rol en el navegador
      localStorage.setItem("userRole", data.role);

      // 🔹 Redirigir según el rol
      if (data.role === "admin") {
        window.location.href = "admin.html";
      } else {
        window.location.href = "user.html";
      }
    } else {
      alert("❌ " + data.message);
    }
  } catch (error) {
    alert("⚠️ Error al conectar con el servidor Flask.");
    console.error(error);
  }
});
