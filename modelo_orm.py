from flask import Flask, render_template, redirect, url_for, request, flash
from peewee import *
from datetime import date

# Configuración de Flask y Base de Datos
app = Flask(__name__)
app.secret_key = 'clave_secreta'
db = SqliteDatabase('recetas.db')

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
    imagen = CharField(default='/static/default_recipe.jpg')
    fecha_publicacion = DateField(default=date.today)
    id_categoria = ForeignKeyField(Categoria, backref='recetas')

# Inicializar la base de datos
def inicializar_db():
    db.connect()
    db.create_tables([Categoria, Receta], safe=True)
    categorias_default = [
        "Todas las recetas", "Entradas", "Platos principales", "Postres", "Bebidas", 
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

@app.route('/consultar_recetas', methods=['GET'])
def consultar_recetas():
    # Consultar todas las recetas con su categoría
    recetas = (Receta
               .select(Receta, Categoria)
               .join(Categoria)
               .order_by(Receta.fecha_publicacion.desc()))
    
    return render_template('Consultar_recetas.html', recetas=recetas)

@app.route('/receta/<int:id_receta>', methods=['GET'])
def detalle_receta(id_receta):
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

    return render_template('detalle_receta.html', receta=receta)

@app.route('/cargar_receta', methods=['GET', 'POST'])
def cargar_receta():
    # Ruta para cargar una nueva receta
    if request.method == 'POST':
        nombre_receta = request.form.get('nombre_receta')
        ingredientes = request.form.get('ingredientes')
        preparacion = request.form.get('preparacion')
        id_categoria = request.form.get('id_categoria')
        imagen = request.form.get('imagen') or '/static/default_recipe.jpg'
        
        if not (nombre_receta and ingredientes and preparacion and id_categoria):
            flash("Todos los campos son obligatorios.", "danger")
            return redirect(url_for('cargar_receta'))

        # Insertar la receta en la base de datos
        Receta.create(
            nombre_receta=nombre_receta,
            ingredientes=ingredientes,
            preparacion=preparacion,
            imagen=imagen,
            id_categoria=id_categoria,
            fecha_publicacion=date.today()
        )
        flash("Receta cargada exitosamente.", "success")
        return redirect(url_for('consultar_recetas'))
    
    categorias = Categoria.select()
    return render_template('Carga_de_receta.html', categorias=categorias)

# Inicializar la base de datos y ejecutar la app
if __name__ == '__main__':
    inicializar_db()
    app.run(debug=True)