from flask import Flask, request, redirect, url_for, render_template, jsonify
from peewee import *
from datetime import date, datetime
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

@app.route('/recetas/<categoria>', methods=['GET'])
@app.route('/recetas', defaults={'categoria': None}, methods=['GET'])
def mostrar_recetas(categoria):
    try:
        # Si no se proporciona una categoría, mostrar todas las recetas
        if not categoria or categoria.lower() == 'todas_las_recetas':
            recetas = Recetas.select().order_by(Recetas.fecha_publicacion.desc())
        else:
            # Filtrar por categoría
            categoria_obj = Categorias.get_or_none(Categorias.nombre_categoria == categoria.replace('_', ' ').title())
            if not categoria_obj:
                return render_template('Consultar_receta.html', recetas=[], mensaje="¡Lo siento! No hay recetas cargadas todavía.")
            
            recetas = Recetas.select().where(Recetas.id_categoria == categoria_obj.id_categoria)

        # Pasar las recetas al template
        return render_template('Consultar_receta.html', recetas=recetas, mensaje=None)

    except Exception as e:
        return f"Error inesperado: {str(e)}", 500