document.addEventListener("DOMContentLoaded", function() {
  // Cargar recetas al inicio
  cargarRecetas('todas_las_recetas');

  // Obtener categorías desde el backend (simulado aquí como un array estático)
  const categorias = [
    "Entradas", "Platos principales", "Postres", "Bebidas", "Sopas", "Panadería", 
    "Pastelería", "Galletas", "Salsas", "Ensaladas", "Guarniciones", "Vegetarianas", "Sin gluten", "Apto para diabéticos"
  ];

  // Añadir categorías al menú
  const menuCategorias = document.getElementById("menu-categorias");
  categorias.forEach(categoria => {
    const li = document.createElement("li");
    li.classList.add("nav-item");
    const a = document.createElement("a");
    a.classList.add("nav-link", "text-white");
    a.href = "#";
    a.textContent = categoria;
    a.addEventListener("click", function() {
      cargarRecetas(categoria.toLowerCase().replace(' ', '_'));
    });
    li.appendChild(a);
    menuCategorias.appendChild(li);
  });

  // Función para cargar recetas por categoría
  function cargarRecetas(categoria) {
    fetch('http://127.0.0.1:5000/recetas/todas_las_recetas')
      .then(response => response.json())
      .then(data => {
        const recetasContainer = document.getElementById("recetas-container");
        recetasContainer.innerHTML = ''; // Limpiar contenido anterior

        if (data.recetas.length === 0) {
          const mensaje = document.createElement('p');
          mensaje.textContent = "¡Lo siento! No tengo receta cargada.";
          recetasContainer.appendChild(mensaje);
        } else {
          data.recetas.forEach(receta => {
            const recetaDiv = document.createElement("div");
            recetaDiv.classList.add("receta");

            const h2 = document.createElement("h3");
            h2.textContent = receta.nombre_receta;
            recetaDiv.appendChild(h2);

            const img = document.createElement("img");
            img.src = receta.imagen;
            img.alt = `Imagen de ${receta.nombre_receta}`;
            img.width = 200;
            recetaDiv.appendChild(img);

            const pIngredientes = document.createElement("p");
            pIngredientes.innerHTML = `<strong>Ingredientes:</strong> ${receta.ingredientes}`;
            recetaDiv.appendChild(pIngredientes);

            const pPreparacion = document.createElement("p");
            pPreparacion.innerHTML = `<strong>Preparación:</strong> ${receta.preparacion}`;
            recetaDiv.appendChild(pPreparacion);

            recetasContainer.appendChild(recetaDiv);
          });
        }
      })
      .catch(error => {
        console.error('Error al cargar las recetas:', error);
        const recetasContainer = document.getElementById("recetas-container");
        recetasContainer.innerHTML = "<p>Error al cargar las recetas.</p>";
      });
  }
});