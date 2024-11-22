from flask import Flask, render_template, request
from peewee import *
from datetime import datetime
import os

# Cargar la variable de entorno que contiene la ruta de la base de datos
db_path = os.getenv('DB_PATH', 'recetas.db')

# Conectar a la base de datos SQLite usando la ruta de la variable de entorno
db = SqliteDatabase(db_path)

# Configurar la base de datos
db = SqliteDatabase('recetas.db')

# Definir las clases de modelos
class Categoria(Model):
    id_categoria = AutoField()
    nombre_categoria = CharField(unique=True)

    class Meta:
        database = db

class Receta(Model):
    id_receta = AutoField()
    nombre_receta = CharField()
    ingredientes = TextField()
    preparacion = TextField()
    imagen = CharField(null=True)
    fecha_publicacion = DateField(default=datetime.now)
    id_categoria = ForeignKeyField(Categoria, backref='recetas')

    class Meta:
        database = db

# Inicializar la app Flask
app = Flask(__name__)

@app.route('/consultar_recetas', methods=['GET'])
def consultar_recetas():
    # Obtener los parámetros de búsqueda desde el query string (si existen)
    nombre_receta = request.args.get('nombre_receta', '')
    ingrediente = request.args.get('ingrediente', '')
    categoria = request.args.get('category', '')
    
    # Página actual (por defecto es la primera)
    page = request.args.get('page', 1, type=int)

    # Número de recetas por página
    recetas_por_pagina = 6

    # Consultar recetas con los filtros aplicados
    query = Receta.select().join(Categoria).where(
        (Receta.nombre_receta.contains(nombre_receta)) &
        (Receta.ingredientes.contains(ingrediente)) &
        (Categoria.nombre_categoria.contains(categoria))
    )

    # Obtener el total de recetas (sin paginar)
    total_recetas = query.count()

    # Calcular el número total de páginas
    total_paginas = (total_recetas + recetas_por_pagina - 1) // recetas_por_pagina

    # Obtener las recetas para la página actual
    recetas = query.paginate(page, recetas_por_pagina)

    return render_template('Consultar_recetas.html', 
                           recetas=recetas,
                           total_paginas=total_paginas,
                           pagina_actual=page)

@app.route('/ver_receta/<int:receta_id>', methods=['GET'])
def ver_receta(receta_id):
    receta = Receta.get(Receta.id_receta == receta_id)
    return render_template('ver_receta.html', receta=receta)

# Ejecutar la app
if __name__ == '__main__':
    app.run(debug=True)