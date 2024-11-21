from flask import Flask, render_template, request, redirect, url_for, flash
from peewee import *
from datetime import date

# Configuración de la aplicación Flask
app = Flask(__name__)
app.secret_key = "clave_secreta_para_flask"

# Conexión a la base de datos
db = SqliteDatabase('recetas.db')

# Modelo base
class BaseModel(Model):
    class Meta:
        database = db

# Tabla Categorías
class Categoria(BaseModel):
    id_categoria = AutoField()  # PK autoincremental
    nombre_categoria = CharField(unique=True)

# Tabla Recetas
class Receta(BaseModel):
    id_receta = AutoField()  # PK autoincremental
    nombre_receta = CharField()
    ingredientes = TextField()
    preparacion = TextField()
    imagen = CharField()  # Ruta o nombre del archivo de imagen
    id_categoria = ForeignKeyField(Categoria, backref='recetas')
    fecha_publicacion = DateField(default=date.today)

# Crear tablas e insertar categorías
def inicializar_base_datos():
    with db:
        db.create_tables([Categoria, Receta])
        # Insertar categorías por única vez
        categorias = [
            "Entradas", "Platos principales", "Postres", "Bebidas",
            "Sopas", "Panadería", "Pastelería", "Galletas", "Salsas", "Ensaladas",
            "Guarniciones", "Vegetarianas", "Sin gluten", "Apto para diabéticos"
        ]
        with db.atomic():
            for nombre in categorias:
                Categoria.get_or_create(nombre_categoria=nombre)

# Ruta para el formulario de carga de receta
@app.route('/cargar_receta', methods=['GET', 'POST'])
def cargar_receta():
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre_receta = request.form['recipeName']
        ingredientes = request.form['ingredients']
        preparacion = request.form['preparation']
        categoria = request.form['category']
        imagen = request.files['image']

        # Validar si se seleccionó una categoría válida
        try:
            categoria_obj = Categoria.get(Categoria.nombre_categoria == categoria)
        except Categoria.DoesNotExist:
            flash("Categoría seleccionada no válida.", "danger")
            return redirect(url_for('cargar_receta'))

        # Guardar la imagen con un nombre único
        imagen_nombre = f"static/images/{imagen.filename}"
        imagen.save(imagen_nombre)

        # Guardar los datos en la base de datos
        Receta.create(
            nombre_receta=nombre_receta,
            ingredientes=ingredientes,
            preparacion=preparacion,
            imagen=imagen_nombre,
            id_categoria=categoria_obj,
            fecha_publicacion=date.today()
        )

        flash("Receta cargada exitosamente.", "success")
        return redirect(url_for('cargar_receta'))

    # Si es GET, mostrar el formulario
    categorias = Categoria.select()
    return render_template('Carga_de_receta.html', categorias=categorias)

# Inicio de la aplicación
if __name__ == '__main__':
    inicializar_base_datos()
    app.run(debug=True)