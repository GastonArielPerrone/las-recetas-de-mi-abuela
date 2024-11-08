from peewee import *
from datetime import datetime
from bs4 import BeautifulSoup # type: ignore

# Configurar la base de datos con Peewee
db = SqliteDatabase('recetas.db')

# Definir el modelo de la tabla Categorias
class Categoria(Model):
    nombre_categoria = CharField()

    class Meta:
        database = db

# Definir el modelo de la tabla Recetas
class Receta(Model):
    nombre_receta = CharField()
    imagen = CharField()  # Ruta de la imagen
    ingredientes = TextField()  # Lista de ingredientes (puede ser texto)
    preparacion = TextField()  # Instrucciones de preparación
    id_categoria = ForeignKeyField(Categoria, backref='recetas')
    fecha_publicacion = DateTimeField(default=datetime.now)

    class Meta:
        database = db

# Conectar a la base de datos
db.connect()

# Obtener las recetas, ordenadas por fecha de publicación (más recientes primero)
recetas = Receta.select().order_by(Receta.fecha_publicacion.desc())

# Abrir el archivo HTML existente
with open('Consultar_recetas.html', 'r', encoding='utf-8') as file:
    html_doc = file.read()

# Usar BeautifulSoup para parsear el HTML
soup = BeautifulSoup(html_doc, 'html.parser')

# Encontrar el contenedor donde insertar las recetas
# Supongamos que tienes un <div id="recetas-container"></div> en tu HTML
recetas_container = soup.find(id="recetas-container")

# Si no hay recetas en la base de datos, agregar el mensaje correspondiente
if not recetas:
    recetas_container.append("<p>Por el momento no hay receta. Disculpe el tiempo perdido.</p>")
else:
    # Si hay recetas, agregar los detalles de cada una
    for receta in recetas:
        receta_div = soup.new_tag("div")
        receta_div.append(f"<h2>{receta.nombre_receta}</h2>")
        receta_div.append(f'<img src="{receta.imagen}" alt="Imagen de {receta.nombre_receta}" width="200">')
        receta_div.append(f"<p><strong>Categoria:</strong> {receta.id_categoria.nombre_categoria}</p>")
        receta_div.append(f"<p><strong>Ingredientes:</strong><br>{receta.ingredientes}</p>")
        receta_div.append(f"<p><strong>Preparación:</strong><br>{receta.preparacion}</p>")
        
        # Insertar la receta en el contenedor
        recetas_container.append(receta_div)

# Guardar el archivo HTML actualizado
with open('Consultar_recetas.html', 'w', encoding='utf-8') as file:
    file.write(str(soup))

# Cerrar la conexión con la base de datos
db.close()

print("Archivo HTML actualizado correctamente.")