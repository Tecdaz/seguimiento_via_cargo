# Seguimiento Via Cargo Bot

Este proyecto es un bot de Telegram que extrae un número de seguimiento de una imagen, busca la información del envío en la web de Via Cargo y devuelve el estado al usuario.

## Configuración para Desarrollo Local (con uv)

1.  **Crear y Activar Entorno Virtual:**
    ```bash
    # Crear el entorno virtual en una carpeta .venv
    uv venv

    # Activar el entorno (en Linux/macOS)
    source .venv/bin/activate
    
    # En Windows (Command Prompt) usa:
    # .venv\Scripts\activate.bat
    ```

2.  **Instalar Dependencias:**
    Las dependencias están definidas en `pyproject.toml`. Para el desarrollo local, necesitas instalar las dependencias base y las del grupo `local` (que incluye Playwright).
    ```bash
    uv pip install -e
    ```

3.  **Instalar los Navegadores de Playwright:**
    Este paso es requerido por Playwright para funcionar.
    ```bash
    playwright install --with-deps
    ```

4.  **Configurar Variables de Entorno:**
    Crea un archivo `.env` en la raíz del proyecto o expórtalas en tu terminal. El bot no funcionará sin estas claves.
    ```bash
    export TELEGRAM_TOKEN="TU_TOKEN_DE_TELEGRAM"
    export OPENAI_API_KEY="TU_API_KEY_DE_OPENAI"
    ```

5.  **Ejecutar el Bot:**
    ```bash
    python3 main.py
    ```

## Uso con Docker

Puedes ejecutar la aplicación dentro de un contenedor de Docker para un despliegue limpio y aislado.

### 1. Construir la Imagen

Este comando construye la imagen de Docker a partir del `Dockerfile`. La etiqueta `-t bot-via-cargo` le da un nombre fácil de recordar.

```bash
docker build -t bot-via-cargo .
```

### 2. Ejecutar el Contenedor

Para ejecutar el bot, necesitas pasarle las claves de API de forma segura.

**a) Crea un archivo `.env`**

En la raíz de tu proyecto, crea un archivo llamado `.env` con tus claves:

```
TELEGRAM_TOKEN=TU_TOKEN_DE_TELEGRAM
OPENAI_API_KEY=TU_API_KEY_DE_OPENAI
```

**b) Inicia el contenedor**

Este comando inicia el contenedor y le pasa las variables de entorno desde tu archivo `.env`.

```bash
docker run --env-file .env --rm -it seguimiento-bot
```

*   `--env-file .env`: Carga las variables de entorno desde tu archivo.
*   `--rm`: Elimina el contenedor automáticamente cuando se detiene.
*   `-it`: Ejecuta el contenedor en modo interactivo para que puedas ver los logs.
