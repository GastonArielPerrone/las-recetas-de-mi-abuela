from flask import Flask, render_template, request, redirect, url_for
from peewee import Model, SqliteDatabase, CharField, AutoField, ForeignKeyField, DateField, PrimaryKeyField
from datetime import date
import os

# Configuración de la base de datos.
db = SqliteDatabase('recetas.db')

# Definición del modelo base
class BaseModel(Model):
    class Meta:
        database = db

# Modelo para la tabla Categorias
class Categoria(BaseModel):
    id_categoria = AutoField(primary_key=True)
    nombre_categoria = CharField(unique=True)

# Modelo para la tabla Recetas
class Receta(BaseModel):
    id_receta = AutoField(primary_key=True)
    nombre_receta = CharField()
    imagen_receta = CharField()  # Ruta de la imagen
    ingredientes = CharField()
    preparacion = CharField()
    fecha_subida = DateField(default=date.today)  # Fecha automática
    id_categoria = ForeignKeyField(Categoria, backref='recetas', null=False)

# Crear la aplicación Flask
app = Flask(__name__, static_folder='static')

# Asegurar que la carpeta de imágenes existe
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configuración de Flask
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Página de inicio
@app.route('/')
def inicio():
    return render_template('index.html')

# Página de consulta de recetas
@app.route('/consultar_recetas', methods=['GET'])
def consultar_recetas():
    # Recuperar los parámetros de búsqueda
    ingrediente = request.args.get('ingredients')
    nombre_receta = request.args.get('recipeName')
    categoria = request.args.get('category')

    # Construir la consulta según los parámetros
    query = Receta.select()

    if ingrediente:
        query = query.where(Receta.ingredientes.contains(ingrediente))
    elif nombre_receta:
        query = query.where(Receta.nombre_receta.contains(nombre_receta))
    elif categoria:
        query = query.join(Categoria).where(Categoria.nombre_categoria == categoria)

    # Ejecutar la consulta y convertir a lista
    recetas = list(query)

    # Renderizar la plantilla con los resultados
    return render_template('Consultar_recetas.html',recetas=recetas)

# Cargar una nueva receta
@app.route('/cargar_receta', methods=['GET', 'POST'])
def cargar_receta():
    try:
        if request.method == 'POST':
            # Obtener datos del formulario
            nombre_receta = request.form.get('recipeName')
            ingredientes = request.form.get('ingredients')
            preparacion = request.form.get('preparation')
            id_categoria = request.form.get('category')

            # Validar campos obligatorios
            if not (nombre_receta and ingredientes and preparacion and id_categoria):
                return "Todos los campos son obligatorios.", 400

            # Manejar la subida de la imagen
            imagen = request.files.get('image')
            if imagen:
                if imagen.filename == '':
                    return "No se seleccionó una imagen", 400
                if not imagen.filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
                    return "El archivo debe ser una imagen válida", 400
                ruta_imagen = os.path.join(app.config['UPLOAD_FOLDER'], imagen.filename)
                imagen.save(ruta_imagen)
            else:
                return "Se requiere una imagen", 400

            # Guardar receta en la base de datos
            Receta.create(
                nombre_receta=nombre_receta,
                ingredientes=ingredientes,
                preparacion=preparacion,
                imagen_receta=ruta_imagen,
                id_categoria=id_categoria
            )
            return redirect(url_for('inicio'))

        # Si el método es GET, renderizar la página
        categorias = Categoria.select()
        return render_template('Carga_de_receta.html', categorias=categorias)
    except Exception as e:
        return f"Error al cargar la receta: {str(e)}", 500

# Inicialización de la base de datos y categorías
def inicializar_bd():
    db.connect()
    db.create_tables([Categoria, Receta])
    # Insertar categorías únicas si no existen
    categorias = [
        "Entradas", "Platos principales", "Postres", "Bebidas", "Sopas",
        "Panadería", "Pastelería", "Galletas", "Salsas", "Ensaladas",
        "Guarniciones", "Vegetarianas", "Sin gluten", "Apto para diabéticos"
    ]
    for nombre in categorias:
        Categoria.get_or_create(nombre_categoria=nombre)
    db.close()

# Inicializar la base de datos al iniciar la app
if __name__ == '__main__':
    print("Rutas registradas:")
    print(app.url_map)
    inicializar_bd()
    app.run(host="0.0.0.0", port=8000, debug=True)