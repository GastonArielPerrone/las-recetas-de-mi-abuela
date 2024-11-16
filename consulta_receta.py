from flask import Flask, render_template
from peewee import *
from datetime import date
from bs4 import BeautifulSoup

app = Flask(__name__)

# Conexión con la base de datos SQLite
db = SqliteDatabase('recetas.db')

# Definición del modelo Categorías
class Categorias(Model):
    id_categoria = AutoField()
    nombre_categoria = CharField(unique=True)

    class Meta:
        database = db

# Definición del modelo Recetas
class Recetas(Model):
    id_receta = AutoField()
    nombre_receta = CharField()
    id_categoria = ForeignKeyField(Categorias, backref='recetas')
    ingredientes = TextField()  # Ingredientes de la receta
    preparacion = TextField()   # Preparación de la receta
    imagen = CharField(null=True)  # URL de la imagen (si existe)
    fecha_publicacion = DateField(default=date.today)

    class Meta:
        database = db

# Conectar a la base de datos
db.connect()

@app.route('/recetas')
def mostrar_recetas():
    try:
        recetas = Recetas.select().order_by(Recetas.fecha_publicacion.desc())
        
        # Manipulación del contenido HTML con BeautifulSoup
        recetas_html = ""
        for receta in recetas:
            # Crea un bloque de HTML para cada receta
            receta_html = f"""
            <div class="receta">
                <h3>{receta.nombre_receta}</h3>
                {f'<img src="{receta.imagen}" alt="Imagen de {receta.nombre_receta}" width="200">' if receta.imagen else ''}
                <p><strong>Ingredientes:</strong> {receta.ingredientes}</p>
                <p><strong>Preparación:</strong> {receta.preparacion}</p>
            </div>
            """
            # Procesa el HTML con BeautifulSoup
            soup = BeautifulSoup(receta_html, 'html.parser')
            recetas_html += str(soup)

        # Devolver el HTML procesado al cliente
        return render_template('Consultar_recetas.html', recetas_html=recetas_html, mensaje=None)
    
    except Exception as e:
        return f"Error inesperado: {str(e)}", 500

@app.route('/recetas/<categoria>')
def recetas_por_categoria(categoria):
    try:
        categoria_obj = Categorias.get_or_none(Categorias.nombre_categoria == categoria.replace('_', ' ').title())
        if not categoria_obj:
            return render_template('Consultar_recetas.html', recetas_html="", mensaje="¡Lo siento! No hay recetas cargadas para esta categoría.")
        
        recetas = Recetas.select().where(Recetas.id_categoria == categoria_obj.id_categoria).order_by(Recetas.fecha_publicacion.desc())
        
        # Manipulación del contenido HTML con BeautifulSoup
        recetas_html = ""
        for receta in recetas:
            receta_html = f"""
            <div class="receta">
                <h3>{receta.nombre_receta}</h3>
                {f'<img src="{receta.imagen}" alt="Imagen de {receta.nombre_receta}" width="200">' if receta.imagen else ''}
                <p><strong>Ingredientes:</strong> {receta.ingredientes}</p>
                <p><strong>Preparación:</strong> {receta.preparacion}</p>
            </div>
            """
            soup = BeautifulSoup(receta_html, 'html.parser')
            recetas_html += str(soup)

        return render_template('Consultar_recetas.html', recetas_html=recetas_html, mensaje=None)
    
    except Exception as e:
        return f"Error inesperado: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)