# Usa una imagen base de Python
FROM python:3.12-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . /app

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expón el puerto en el que se ejecutará la aplicación
EXPOSE 5000

# Ejecuta la aplicación usando Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "carga_consulta_receta:app"]
