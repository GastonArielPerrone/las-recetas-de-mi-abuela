from flask import Flask, jsonify
from peewee import *
from datetime import datetime, date
from flask_cors import CORS

app = Flask(__name__)

app.route('/')
def home():
    return "Bienvenid@ a la API de todas las recetas."

# Configuración de la base de datos
db = SqliteDatabase('recetas.db')

class Categorias(Model):
    id_categoria = AutoField()
    nombre_categoria = CharField(unique=True)
    class Meta:
        database = db

class Recetas(Model):
    id_receta = AutoField()
    nombre_receta = CharField()
    id_categoria = ForeignKeyField(Categorias, backref='recetas')
    ingredientes = TextField()  # Agregar ingredientes
    preparacion = TextField()   # Agregar preparación
    imagen = CharField(null=True)  # Agregar imagen, si la necesitas
    fecha_publicacion = DateField(default=date.today)

    class Meta:
        database = db

# Conectar a la base de datos
db.connect()

@app.route('/recetas/todas-las-recetas', methods=['GET'])
def obtener_todas_las_recetas():
    recetas = Recetas.select().join(Categorias).order_by(Recetas.fecha_publicacion.desc())
    recetas_list = [{
        'nombre_receta': receta.nombre_receta,
        'imagen': receta.imagen,
        'ingredientes': receta.ingredientes,
        'preparacion': receta.preparacion
    } for receta in recetas]
    return jsonify({'recetas': recetas_list})

@app.route('/recetas/<categoria>', methods=['GET'])
def obtener_recetas_por_categoria(categoria):
    categoria_obj = Categorias.get_or_none(Categorias.nombre_categoria == categoria.replace('_', ' ').title())
    if categoria_obj:
        recetas = Recetas.select().where(Recetas.id_categoria == categoria_obj)
        recetas_list = [{
            'nombre_receta': receta.nombre_receta,
            'imagen': receta.imagen,
            'ingredientes': receta.ingredientes,
            'preparacion': receta.preparacion
        } for receta in recetas]
        return jsonify({'recetas': recetas_list})
    else:
        return jsonify({'recetas': []})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)