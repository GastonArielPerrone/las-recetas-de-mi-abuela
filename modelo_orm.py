from flask import Flask, render_template, request, redirect, url_for
from peewee import Model, SqliteDatabase, CharField, AutoField, ForeignKeyField, DateField
from datetime import date

# Configuración de la base de datos
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
    id_categoria = ForeignKeyField(Categoria, backref='recetas')

# Crear la aplicación Flask
app = Flask(__name__)

# Carga de página de inicio
@app.route('/')
def inicio():
    return render_template('index.html')

# Carga de página de Consultas.
app.route('/Consultar_recetas')
def consultar_recetas():
    return render_template('Consultar_recetas.html')

# Ruta principal para mostrar el formulario
app.route('/Carga_de_receta')
def carga_de_receta():
    return render_template('Carga_de_receta.html')

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

# Ruta para manejar la carga de recetas
@app.route('/Carga_de_receta.html', methods=['GET','POST'])
def carga_receta():
    try:
        # Obtener datos del formulario
        nombre_receta = request.form['recipeName']
        ingredientes = request.form['ingredients']
        preparacion = request.form['preparation']
        id_categoria = request.form['category']
        
        # Manejar la subida de la imagen
        imagen = request.files['image']
        if imagen:
            ruta_imagen = f'static/uploads/{imagen.filename}'
            imagen.save(ruta_imagen)
        else:
            ruta_imagen = ''

        # Guardar receta en la base de datos
        Receta.create(
            nombre_receta=nombre_receta,
            ingredientes=ingredientes,
            preparacion=preparacion,
            imagen_receta=ruta_imagen,
            id_categoria=id_categoria
        )
        return redirect(url_for('carga_de_receta'))
    except Exception as e:
        return f"Error al cargar la receta: {str(e)}"

# Inicializar la base de datos al iniciar la app
if __name__ == '__main__':
    inicializar_bd()
    app.run(host="0.0.0.0", port=3000,debug=True)