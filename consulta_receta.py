from peewee import *
from datetime import datetime
from bs4 import BeautifulSoup

# Configuración de la base de datos
db = SqliteDatabase('recetas.db')

class Categorias(Model):
    nombre_categoria = CharField()

    class Meta:
        database = db

class Recetas(Model):
    nombre_receta = CharField()
    imagen = CharField()
    ingredientes = TextField()
    preparacion = TextField()
    id_categoria = ForeignKeyField(Categorias, backref='recetas')
    fecha_publicacion = DateTimeField(default=datetime.now)

    class Meta:
        database = db

# Conectar a la base de datos
db.connect()

# Obtener las categorías de la base de datos
categorias = Categorias.select()

# Iterar sobre cada categoría para generar una página HTML para ella
for categoria in categorias:
    # Crear el nombre del archivo HTML para cada categoría (ej. entradas.html)
    archivo_html = f"{categoria.nombre_categoria.lower().replace(' ', '_')}.html"
    
    # Crear el contenido HTML básico con BeautifulSoup
    soup = BeautifulSoup("<html><body></body></html>", 'html.parser')
    
    # Ahora estamos seguros de que <body> existe
    assert soup.body is not None  # Aseguramos que <body> existe al crear el soup
    
    # Crear el encabezado
    header = soup.new_tag("h1")
    header.string = f"Recetas de {categoria.nombre_categoria}"
    soup.body.append(header)

    # Crear el subtítulo con el nombre de la categoría seleccionada
    subtitle = soup.new_tag("h2")
    subtitle.string = f"Categoría: {categoria.nombre_categoria}"
    soup.body.append(subtitle)
    
    # Crear el menú de categorías
    nav = soup.new_tag("nav")
    ul = soup.new_tag("ul")
    
    # Agregar las categorías al menú de navegación
    for cat in categorias:
        li = soup.new_tag("li")
        a = soup.new_tag("a", href=f"{cat.nombre_categoria.lower().replace(' ', '_')}.html")
        a.string = cat.nombre_categoria
        li.append(a)
        ul.append(li)
    
    nav.append(ul)
    soup.body.append(nav)
    
    # Obtener las recetas de esta categoría
    recetas_categoria = Recetas.select().where(Recetas.id_categoria == categoria).order_by(Recetas.fecha_publicacion.desc())
    
    # Verificar si hay recetas para esta categoría
    if not recetas_categoria.exists():
        no_recetas_message = soup.new_tag("p")
        no_recetas_message.string = f"¡Lo siento! La categoría {categoria.nombre_categoria} no tiene receta."
        soup.body.append(no_recetas_message)
    else:
        # Intentar encontrar el contenedor de recetas
        recetas_container = soup.find(id="recetas-container")
        
        # Si no existe el contenedor, lo creamos
        if recetas_container is None:
            recetas_container = soup.new_tag("div", id="recetas-container")
            soup.body.append(recetas_container)  # Aseguramos que el contenedor sea parte del body

        # Agregar las recetas al contenedor
        for receta in recetas_categoria:
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
            strong_categoria.string = "Categoría: "
            p_categoria.append(strong_categoria)
            p_categoria.append(categoria.nombre_categoria)
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
            
            # Agregar la receta al contenedor
            recetas_container.append(receta_div)
    
    # Guardar el archivo HTML para esta categoría
    try:
        with open(archivo_html, 'w', encoding='utf-8') as file:
            file.write(str(soup))
        print(f"Archivo HTML para la categoría {categoria.nombre_categoria} guardado como {archivo_html}.")
    except IOError as e:
        print(f"Error al guardar el archivo para {categoria.nombre_categoria}: {e}")

# Cerrar la conexión con la base de datos
db.close()