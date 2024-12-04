from flask import Flask, render_template, redirect, url_for, request, flash
from peewee import *
from datetime import date
import os

# Configuración de Flask y Base de Datos
app = Flask(__name__, static_folder='static')
app.secret_key = 'clave_secreta'
db = SqliteDatabase('recetas.db')

# Carpeta para subir imágenes
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Modelos de la base de datos
class BaseModel(Model):
    class Meta:
        database = db

class Categoria(BaseModel):
    id_categoria = AutoField()
    nombre_categoria = CharField(unique=True)

class Receta(BaseModel):
    id_receta = AutoField()
    nombre_receta = CharField()
    ingredientes = TextField()
    preparacion = TextField()
    imagen = CharField(default='uploads/default_recipe.jpg')
    fecha_publicacion = DateField(default=date.today)
    id_categoria = ForeignKeyField(Categoria, backref='recetas')

# Inicializar la base de datos
def inicializar_db():
    db.connect()
    db.create_tables([Categoria, Receta], safe=True)
    categorias_default = [
        "Entradas", "Platos principales", "Postres", "Bebidas",
        "Sopas", "Panadería", "Pastelería", "Galletas", "Salsas", "Ensaladas",
        "Guarniciones", "Vegetarianas", "Sin gluten", "Apto para diabéticos"
    ]
    for cat in categorias_default:
        Categoria.get_or_create(nombre_categoria=cat)
    db.close()

# Rutas
@app.route('/')
def inicio():
    return render_template('index.html')  # Página principal

@app.route('/consultar_recetas')
def consultar_recetas():
    return render_template('Consultar_recetas.html')

@app.route('/carga_de_receta')
def carga_de_receta():
    categorias = Categoria.select()
    return render_template('Carga_de_receta.html', categorias=categorias)

@app.route('/Carga_de_receta.html', methods=['GET', 'POST'])
def Carga_de_receta():
    db.connect()
    if request.method == 'POST':
        nombre_receta = request.form.get('recipeName')
        ingredientes = request.form.get('ingredients')
        preparacion = request.form.get('preparation')
        nombre_categoria = request.form.get('category')
        imagen = request.files['image']

        if not (nombre_receta and ingredientes and preparacion and nombre_categoria and imagen):
            flash("Todos los campos son obligatorios.", "danger")
            return redirect(url_for('carga_de_receta'))

        # Obtener la categoría por su nombre
        try:
            categoria = Categoria.get(Categoria.nombre_categoria == nombre_categoria)
        except Categoria.DoesNotExist:
            flash("La categoría seleccionada no existe.", "danger")
            return redirect(url_for('carga_de_receta'))

        # Guardar la imagen
        image_path = 'uploads/default_recipe.jpg'  # Valor por defecto
        if imagen.filename != '':
            image_path = f'uploads/{imagen.filename}'
            imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], imagen.filename))

        # Insertar la receta en la base de datos
        Receta.create(
            nombre_receta=nombre_receta,
            ingredientes=ingredientes,
            preparacion=preparacion,
            imagen=image_path,
            id_categoria=categoria.id_categoria,
            fecha_publicacion=date.today()
        )
        flash("Receta cargada exitosamente.", "success")
        return redirect(url_for('consultar_recetas'))

    categorias = Categoria.select()
    db.close()
    return render_template('Carga_de_receta.html', categorias=categorias)

@app.route('/Consultar_recetas.html', methods=['GET'])
def consultar_recetas_db():
    db.connect()
    # Consultar todas las recetas con su categoría
    recetas = (Receta
               .select(Receta, Categoria)
               .join(Categoria)
               .order_by(Receta.fecha_publicacion.desc()))
    db.close()
    return render_template('Consultar_recetas.html', recetas=recetas)

@app.route('/receta/<int:id_receta>', methods=['GET'])
def detalle_receta(id_receta):
    db.connect()
    # Consultar detalles de una receta específica
    try:
        receta = (Receta
                  .select(Receta, Categoria)
                  .join(Categoria)
                  .where(Receta.id_receta == id_receta)
                  .get())
    except Receta.DoesNotExist:
        flash("La receta no existe.", "danger")
        return redirect(url_for('consultar_recetas'))
    db.close()
    return render_template('detalle_receta.html', receta=receta)

# Inicializar la base de datos y ejecutar la app
if __name__ == '__main__':
    inicializar_db()
    app.run(host='0.0.0.0', port=1500, debug=True)