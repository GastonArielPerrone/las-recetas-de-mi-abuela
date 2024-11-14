fetch('https://las-recetas-de-mi-abuela.onrender.com/api/data')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));