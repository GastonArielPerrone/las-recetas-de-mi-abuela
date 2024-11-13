document.addEventListener("DOMContentLoaded", function() {
  // Función para cargar recetas por categoría
  function cargarRecetas(categoria) {
      fetch(`/recetas/${categoria}`)
          .then(response => response.json())
          .then(data => {
              const recetasContainer = document.getElementById("recetas-container");
              recetasContainer.innerHTML = '';  // Limpiar contenido anterior

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

  // Cargar las recetas al inicio (por ejemplo, todas las recetas)
  cargarRecetas('todas_las_recetas');
});