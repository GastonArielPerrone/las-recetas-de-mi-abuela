document.addEventListener("DOMContentLoaded", function() {
    // Obtenemos las categorías desde el backend (esto se podría hacer con un fetch si tuvieras una API)
    const categorias = [
      "Entradas", "Platos principales", "Postres", "Bebidas", "Sopas", "Panadería", 
      "Pastelería", "Galletas", "Salsas", "Ensaladas", "Guarniciones", "Vegetarianas", "Sin gluten", "Apto para diabéticos"
    ];

    // Añadir las categorías al menú
    const menuCategorias = document.querySelector("ul.nav");
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

    // Función para cargar recetas según la categoría
    function cargarRecetas(categoria) {
      fetch(`/recetas/${categoria}`)
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