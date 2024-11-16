from flask import Flask, request, redirect, url_for, render_template, jsonify
from peewee import *
from datetime import date
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)

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
    ingredientes = TextField()
    preparacion = TextField()
    imagen = CharField(null=True)
    fecha_publicacion = DateField(default=date.today)

    class Meta:
        database = db

# Conectar a la base de datos
db.connect()

logging.basicConfig(
    level=logging.DEBUG,  # Puedes usar DEBUG, INFO, WARNING, ERROR, CRITICAL
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Imprime los logs en la consola
        logging.FileHandler('app.log')  # También guarda los logs en un archivo llamado app.log
    ]
)

@app.route('/')
def home():
    return "Bienvenid@ a la API de todas las recetas."

@app.route('/recetas', methods=['GET'])
@app.route('/recetas', defaults={'categoria': None}, methods=['GET'])
@app.route('/recetas')
def mostrar_recetas():
    try:
        # Suponiendo que ya tienes una base de datos con recetas
        recetas = Recetas.select()  # Obtén las recetas de la base de datos
        return render_template('Consultar_recetas.html', recetas=recetas)
    except Exception as e:
        return f"Error inesperado: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)