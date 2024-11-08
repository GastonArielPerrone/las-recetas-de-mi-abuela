from flask import Flask, request, redirect, url_for, render_template
from peewee import SqliteDatabase, Model, AutoField, CharField, ForeignKeyField, DateField, IntegrityError, DoesNotExist
from datetime import date

# Inicializar la aplicación y la base de datos
app = Flask(__name__)
db = SqliteDatabase('recetas.db')

# Definición del modelo para la tabla Categorias
class BaseModel(Model):
    class Meta:
        database = db

class Categorias(BaseModel):
    id_categoria = AutoField()
    nombre_categoria = CharField(unique=True)

# Definición del modelo para la tabla Recetas
class Recetas(BaseModel):
    id_receta = AutoField()
    nombre_receta = CharField()
    id_categoria = ForeignKeyField(Categorias, backref='recetas')
    fecha_publicacion = DateField()

# Crear las tablas
db.connect()
db.create_tables([Categorias, Recetas])

# Función para agregar las categorías iniciales si no existen
def agregar_categorias():
    categorias = [
        "Todas las recetas", "Entradas", "Platos principales", "Postres", "Bebidas", "Sopas",
        "Panadería", "Pastelería", "Galletas", "Salsas", "Ensaladas", "Guarniciones",
        "Vegetarianas", "Sin gluten", "Apto para diabéticos"
    ]
    for categoria in categorias:
        Categorias.get_or_create(nombre_categoria=categoria)

# Ejecutar la función para asegurar que las categorías existen en la base de datos
agregar_categorias()

# Ruta para cargar la receta desde el formulario HTML
@app.route('/cargar_receta', methods=['POST'])
def cargar_receta():
    try:
        # Obtener datos del formulario
        nombre_receta = request.form['recipeName']
        categoria_nombre = request.form['category']
        ingredientes = request.form['ingredients']
        preparacion = request.form['preparation']
        
        # Buscar el id de la categoría seleccionada
        categoria = Categorias.get(Categorias.nombre_categoria == categoria_nombre)
        
        # Insertar la receta en la base de datos con el id de la categoría correspondiente
        Recetas.create(
            nombre_receta=nombre_receta,
            id_categoria=categoria.id_categoria,  # Asignación del id de la categoría
            fecha_publicacion=date.today()
        )
        
        return redirect(url_for('cargar_receta'))  # Redirigir después de la carga exitosa
    
    except DoesNotExist:
        return "Error: La categoría seleccionada no existe en la base de datos.", 400
    except IntegrityError:
        return "Error: No se pudo guardar la receta, por favor verifica los datos ingresados.", 400
    except Exception as e:
        return f"Error inesperado: {str(e)}", 500

# Página principal de carga de recetas
@app.route('/')
def cargar_receta_form():
    categorias = Categorias.select()
    return render_template('formulario_receta.html', categorias=categorias)

if __name__ == '__main__':
    app.run(debug=True)