FROM python:3

# Declaro mi directorio de trabajo
WORKDIR /usr/src/app

ENV PYTHONPATH=${PYTHONPATH}:${PWD} 

# Copio los archivos de poetry a /app
COPY  pyproject.toml ./
COPY  poetry.lock ./

# Corro los comandos para instalar poetry
RUN pip3 install poetry
# Este comando deshabilito crear el entorno virtual (ya que estoy con imagenes)
RUN poetry config virtualenvs.create false
# Este comando installa las dependencias que no son de dev y --no-root es para no copiar el proyecto
RUN poetry install --only main --no-root

# Creo una carpeta users_service
RUN mkdir users_service

# Copio todo lo de users_service local a users_service
COPY ./users_service/ ./users_service

# Expongo el puerto de la imagen en 8000
EXPOSE 8000

# Corro comando para levantar el servidor
CMD [ "poetry", "run", "uvicorn", "users_service.app:app"]