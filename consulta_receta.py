from peewee import *
from datetime import datetime
from bs4 import BeautifulSoup  # type: ignore

# Configurar la base de datos con Peewee
db = SqliteDatabase('recetas.db')

# Definir el modelo de la tabla Categorias
class Categoria(Model):
    nombre_categoria = CharField()

    class Meta:
        database = db

# Definir el modelo de la tabla Recetas
class Recetas(Model):
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
recetas = Recetas.select().order_by(Recetas.fecha_publicacion.desc())

# Abrir el archivo HTML existente
with open('Consultar_recetas.html', 'r', encoding='utf-8') as file:
    html_doc = file.read()

# Usar BeautifulSoup para parsear el HTML
soup = BeautifulSoup(html_doc, 'html.parser')

# Encontrar el contenedor donde insertar las recetas
recetas_container = soup.find(id="recetas-container")

# Verificar si el contenedor fue encontrado
if recetas_container is None:
    print("No se encontró el contenedor 'recetas-container'. Creando uno nuevo.")
    # Si no existe, crearlo
    recetas_container = soup.new_tag("div", id="recetas-container")
    # Asegúrate de agregar el contenedor al lugar adecuado en el HTML
    if soup.body:
        soup.body.append(recetas_container)
    else:
        # Si no se encuentra <body>, crea un contenedor raíz
        root = soup.new_tag("body")
        root.append(recetas_container)
        soup.append(root)

# Si no hay recetas en la base de datos, agregar el mensaje correspondiente
if not recetas:
    no_recetas_message = soup.new_tag("p")
    no_recetas_message.string = "Por el momento no hay receta. Disculpe el tiempo perdido."
    recetas_container.append(no_recetas_message)
else:
    # Si hay recetas, agregar los detalles de cada una
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

        # Insertar la receta en el contenedor
        recetas_container.append(receta_div)

# Guardar el archivo HTML actualizado
with open('Consultar_recetas.html', 'w', encoding='utf-8') as file:
    file.write(str(soup))

# Cerrar la conexión con la base de datos
db.close()

print("Archivo HTML actualizado correctamente.")