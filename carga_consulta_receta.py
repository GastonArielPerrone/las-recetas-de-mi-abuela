from flask import Flask, request, render_template, jsonify
from peewee import *
from datetime import date

# Inicializar la aplicación y la base de datos
app = Flask(__name__)
db = SqliteDatabase('recetas.db')

# Modelos de la base de datos
class BaseModel(Model):
    class Meta:
        database = db

class Categorias(BaseModel):
    id_categoria = AutoField()
    nombre_categoria = CharField(unique=True)

class Recetas(BaseModel):
    id_receta = AutoField()
    nombre_receta = CharField()
    id_categoria = ForeignKeyField(Categorias, backref='recetas')
    ingredientes = TextField()
    preparacion = TextField()
    imagen = CharField(null=True)
    fecha_publicacion = DateField(default=date.today)

# Crear las tablas y categorías iniciales
db.connect()
db.create_tables([Categorias, Recetas])
def agregar_categorias():
    categorias = [
        "Todas las recetas", "Entradas", "Platos principales", "Postres", "Bebidas", "Sopas",
        "Panadería", "Pastelería", "Galletas", "Salsas", "Ensaladas", "Guarniciones",
        "Vegetarianas", "Sin gluten", "Apto para diabéticos"
    ]
    for categoria in categorias:
        Categorias.get_or_create(nombre_categoria=categoria)
agregar_categorias()

# Ruta para mostrar el formulario de búsqueda
@app.route('/')
def consultar_recetas_form():
    return render_template('Consultar_recetas.html')

# Ruta para buscar por ingrediente
@app.route('/buscar/ingrediente', methods=['POST'])
def buscar_por_ingrediente():
    ingrediente = request.form.get('ingrediente', '')
    recetas = Recetas.select().where(Recetas.ingredientes.contains(ingrediente))
    if recetas.exists():
        return render_template('Consultar_recetas.html', recetas=recetas)
    else:
        return render_template('Consultar_recetas.html', mensaje="¡Lo siento! No se encuentra la receta deseada.")

# Ruta para buscar por nombre de receta
@app.route('/buscar/nombre', methods=['POST'])
def buscar_por_nombre():
    nombre = request.form.get('nombre-receta', '')
    recetas = Recetas.select().where(Recetas.nombre_receta.contains(nombre))
    if recetas.exists():
        return render_template('Consultar_recetas.html', recetas=recetas)
    else:
        return render_template('Consultar_recetas.html', mensaje="¡Lo siento! No se encuentra la receta deseada.")

# Ruta para buscar por categoría
@app.route('/buscar/categoria', methods=['POST'])
def buscar_por_categoria():
    categoria_nombre = request.form.get('category', '')
    if categoria_nombre == "Todas las recetas":
        recetas = Recetas.select()
    else:
        try:
            categoria = Categorias.get(Categorias.nombre_categoria == categoria_nombre)
            recetas = Recetas.select().where(Recetas.id_categoria == categoria.id_categoria)
        except DoesNotExist:
            recetas = []
    if recetas:
        return render_template('Consultar_recetas.html', recetas=recetas)
    else:
        return render_template('Consultar_recetas.html', mensaje="¡Lo siento! No se encuentra la receta deseada.")

if __name__ == '__main__':
    app.run(debug=True)