from modelo_orm import Receta, Categoria

recetas = (Receta
           .select(Receta, Categoria)
           .join(Categoria))