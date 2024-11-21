from peewee import *
from datetime import date

# Conexión a la base de datos
db = SqliteDatabase('recetas.db')

# Modelo base para conectar las tablas con la base de datos
class BaseModel(Model):
    class Meta:
        database = db

# Tabla Categorías
class Categoria(BaseModel):
    id_categoria = AutoField()  # PK autoincremental
    nombre_categoria = CharField(unique=True)

# Tabla Recetas
class Receta(BaseModel):
    id_receta = AutoField()  # PK autoincremental
    nombre_receta = CharField()
    ingredientes = TextField()
    preparacion = TextField()
    imagen = CharField()  # Ruta o nombre del archivo de imagen
    id_categoria = ForeignKeyField(Categoria, backref='recetas')
    fecha_publicacion = DateField(default=date.today)

# Crear tablas
def crear_tablas():
    with db:
        db.create_tables([Categoria, Receta])
        print("Tablas creadas con éxito.")

# Insertar las categorías una única vez
def insertar_categorias():
    categorias = [
        "Todas las recetas", "Entradas", "Platos principales", "Postres", "Bebidas",
        "Sopas", "Panadería", "Pastelería", "Galletas", "Salsas", "Ensaladas",
        "Guarniciones", "Vegetarianas", "Sin gluten", "Apto para diabéticos"
    ]
    with db.atomic():
        for nombre in categorias:
            Categoria.get_or_create(nombre_categoria=nombre)
        print("Categorías insertadas con éxito.")

if __name__ == '__main__':
    crear_tablas()
    insertar_categorias()