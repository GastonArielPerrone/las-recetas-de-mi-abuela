from modelo_orm import db, Categoria
db.connect()
categorias = Categoria.select()
for cat in categorias:
    print(cat.id_categoria, cat.nombre_categoria)
db.close()