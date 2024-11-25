from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from peewee import *
from datetime import datetime
import os

# Conexión a la base de datos SQLite usando Peewee
db = SqliteDatabase('recetas.db')

# Modelos de Peewee
class Categoria(Model):
    id_categoria = AutoField()
    nombre_categoria = CharField(unique=True)

    class Meta:
        database = db

class Receta(Model):
    id_receta = AutoField()
    nombre_receta = CharField()
    ingredientes = TextField()
    preparacion = TextField()
    imagen = CharField(null=True)
    fecha_publicacion = DateField(default=datetime.now)
    id_categoria = ForeignKeyField(Categoria, backref='recetas')

    class Meta:
        database = db

# Inicialización de la base de datos (si no existen las tablas, las crea)
def initialize_db():
    db.connect()
    db.create_tables([Categoria, Receta], safe=True)

# Configuración de Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images/recetas'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limitar el tamaño de la imagen a 16 MB

initialize_db()

# Ruta para cargar una receta
@app.route('/cargar_receta', methods=['GET', 'POST'])
def cargar_receta_view():
    if request.method == 'POST':
        # Obtener los datos del formulario
        form_data = {
            'recipeName': request.form['recipeName'],
            'ingredients': request.form['ingredients'],
            'preparation': request.form['preparation']
        }

        # Obtener la imagen cargada
        imagen = request.files.get('image')

        if not imagen:
            return "Por favor, sube una imagen", 400

        # Obtener la categoría seleccionada
        categoria_id = request.form['category']

        # Procesar y guardar la imagen en el servidor
        imagen_filename = secure_filename(imagen.filename)
        imagen_path = os.path.join(app.config['UPLOAD_FOLDER'], imagen_filename)
        imagen.save(imagen_path)

        # Crear la receta en la base de datos
        categoria = Categoria.get(Categoria.id_categoria == categoria_id)

        receta = Receta.create(
            nombre_receta=form_data['recipeName'],
            ingredientes=form_data['ingredients'],
            preparacion=form_data['preparation'],
            imagen=imagen_path,
            id_categoria=categoria
        )

        # Redirigir a la página de consulta de recetas
        return redirect(url_for('consultar_recetas'))

    # Si es un GET, mostrar el formulario de carga de recetas
    categorias = Categoria.select()
    return render_template('cargar_receta.html', categorias=categorias)

# Ruta para consultar recetas
@app.route('/consultar_recetas', methods=['GET'])
def consultar_recetas():
    # Obtener parámetros de búsqueda
    nombre_receta = request.args.get('nombre_receta', '')
    categoria = request.args.get('category', '')
    
    # Paginación
    page = request.args.get('page', 1, type=int)
    recetas_por_pagina = 6

    # Filtrar recetas según los parámetros de búsqueda
    query = Receta.select().join(Categoria).where(
        (Receta.nombre_receta.contains(nombre_receta)) &
        (Categoria.nombre_categoria.contains(categoria))
    )

    # Obtener el total de recetas (sin paginar)
    total_recetas = query.count()

    # Calcular el número total de páginas
    total_paginas = (total_recetas + recetas_por_pagina - 1) // recetas_por_pagina

    # Obtener las recetas para la página actual
    recetas = query.paginate(page, recetas_por_pagina)

    return render_template('consultar_recetas.html', 
                           recetas=recetas,
                           total_paginas=total_paginas,
                           pagina_actual=page)

# Ruta para ver una receta específica
@app.route('/ver_receta/<int:receta_id>', methods=['GET'])
def ver_receta(receta_id):
    receta = Receta.get(Receta.id_receta == receta_id)
    return render_template('ver_receta.html', receta=receta)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port= 1000)