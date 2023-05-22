# Usa la imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de código fuente y los requisitos al contenedor
# RUN cd api
COPY . .

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto en el que el servidor FastAPI se ejecutará
EXPOSE 80

# Define el comando para iniciar el servidor FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
