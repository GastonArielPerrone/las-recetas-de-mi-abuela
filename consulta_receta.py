from peewee import *
from datetime import datetime
from bs4 import BeautifulSoup

# Configurar la base de datos con Peewee
db = SqliteDatabase('recetas.db')

class Categoria(Model):
    nombre_categoria = CharField()
    class Meta:
        database = db

class Recetas(Model):
    nombre_receta = CharField()
    imagen = CharField()
    ingredientes = TextField()
    preparacion = TextField()
    id_categoria = ForeignKeyField(Categoria, backref='recetas')
    fecha_publicacion = DateTimeField(default=datetime.now)
    class Meta:
        database = db

# Conectar a la base de datos
db.connect()

# Obtener las recetas
recetas = Recetas.select().order_by(Recetas.fecha_publicacion.desc())

# Cargar el HTML y verificar contenedor
try:
    with open('Consultar_recetas.html', 'r', encoding='utf-8') as file:
        html_doc = file.read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    print("Archivo HTML cargado exitosamente.")
except FileNotFoundError:
    # Crear HTML base si no existe
    print("El archivo no existe. Creando un HTML base.")
    soup = BeautifulSoup("<html><body></body></html>", 'html.parser')

# Verificar y crear 'recetas-container'
recetas_container = soup.find(id="recetas-container")
if recetas_container is None:
    print("No se encontró el contenedor 'recetas-container'. Creando uno nuevo.")
    recetas_container = soup.new_tag("div", id="recetas-container")
    if soup.body:
        soup.body.append(recetas_container)
    else:
        root = soup.new_tag("body")
        root.append(recetas_container)
        soup.append(root)

# Generar contenido HTML para recetas
if not recetas:
    no_recetas_message = soup.new_tag("p")
    no_recetas_message.string = "Por el momento no hay receta. Disculpe el tiempo perdido."
    recetas_container.append(no_recetas_message)
    print("No se encontraron recetas en la base de datos.")
else:
    for receta in recetas:
        receta_div = soup.new_tag("div", attrs={"class": "receta"})

        # Título de la receta
        h2_tag = soup.new_tag("h2")
        h2_tag.string = receta.nombre_receta
        receta_div.append(h2_tag)

        # Imagen de la receta
        img_tag = soup.new_tag("img", src=receta.imagen, alt=f"Imagen de {receta.nombre_receta}", width="200")
        receta_div.append(img_tag)

        # Categoría de la receta
        p_categoria = soup.new_tag("p")
        strong_categoria = soup.new_tag("strong")
        strong_categoria.string = "Categoria: "
        p_categoria.append(strong_categoria)
        p_categoria.append(receta.id_categoria.nombre_categoria)
        receta_div.append(p_categoria)

        # Ingredientes de la receta
        p_ingredientes = soup.new_tag("p")
        strong_ingredientes = soup.new_tag("strong")
        strong_ingredientes.string = "Ingredientes: "
        p_ingredientes.append(strong_ingredientes)
        p_ingredientes.append(receta.ingredientes)
        receta_div.append(p_ingredientes)

        # Preparación de la receta
        p_preparacion = soup.new_tag("p")
        strong_preparacion = soup.new_tag("strong")
        strong_preparacion.string = "Preparación: "
        p_preparacion.append(strong_preparacion)
        p_preparacion.append(receta.preparacion)
        receta_div.append(p_preparacion)

        recetas_container.append(receta_div)
    print("Recetas añadidas exitosamente al contenedor.")

# Guardar el archivo HTML actualizado
try:
    with open('Consultar_recetas.html', 'w', encoding='utf-8') as file:
        file.write(str(soup))
    print("Archivo HTML actualizado correctamente.")
except IOError as e:
    print(f"Error al guardar el archivo: {e}")

# Cerrar conexión con la base de datos
db.close()