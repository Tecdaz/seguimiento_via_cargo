import os
import logging
from openai import AsyncOpenAI
from dotenv import load_dotenv

# --- Configuración de Logging ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv()

# --- Carga de API Keys ---
# Carga las API keys desde variables de entorno para mayor seguridad
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# --- Cliente de OpenAI ---
# Cliente asíncrono de OpenAI
client = None
if OPENAI_API_KEY:
    client = AsyncOpenAI(api_key=OPENAI_API_KEY)
else:
    logger.warning("OPENAI_API_KEY no encontrada. La funcionalidad de OpenAI estará deshabilitada.")
