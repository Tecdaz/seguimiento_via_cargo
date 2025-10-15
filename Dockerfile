# Usar la imagen oficial de Playwright que incluye Python y las dependencias de los navegadores
FROM python:bookworm

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Instalar uv, nuestro gestor de paquetes
RUN pip install uv

# Copiar el archivo que define las dependencias para aprovechar el cache de Docker
COPY pyproject.toml ./

# Instalar las dependencias del proyecto usando uv
# El comando '-e .' instala el proyecto en modo editable y sus dependencias de pyproject.toml
RUN uv pip install -e . --system

# Instalar Playwright
RUN playwright install --with-deps

# Copiar el resto del código de la aplicación al directorio de trabajo
COPY . .

# Comando para ejecutar la aplicación cuando se inicie el contenedor
# Las API keys se pasarán como variables de entorno al ejecutar el contenedor
CMD ["python3", "main.py"]
