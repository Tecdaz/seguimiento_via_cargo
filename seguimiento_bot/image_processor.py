import base64
import hashlib
from collections import deque
from .config import client, logger

# Cache para almacenar los últimos 10 mensajes procesados: (image_hash, extracted_text)
LAST_MESSAGES_CACHE = deque(maxlen=10)

async def extract_text_from_image(image_bytes: bytes) -> str | None:
    """
    Envía una imagen a la API de OpenAI Vision para extraer texto.
    Utiliza un caché para evitar llamadas redundantes con la misma imagen.
    """
    if not client:
        logger.error("Cliente de OpenAI no inicializado. Verifica la API key.")
        return None
    
    # Calcular hash de la imagen
    image_hash = hashlib.sha256(image_bytes).hexdigest()
    
    # Buscar en caché
    for cached_hash, cached_text in LAST_MESSAGES_CACHE:
        if cached_hash == image_hash:
            logger.info("Imagen encontrada en caché. Retornando texto almacenado.")
            return cached_text

    logger.info("Enviando imagen a OpenAI para extracción de texto...")
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
   
    
    try:
        response = await client.responses.create(
            model="gpt-5-nano",
            instructions="Extrae el número de seguimiento o guía de la imagen suministrada, el mismo se encuentra debajo del codigo de barras ubicado en la parte superior derecha despues de las letras 'GUIA No.' y se compone de 12 digitos. Devuelve únicamente el número, sin texto adicional.",
            input=[
                {
                    'role': 'user',
                    'content': [
                        {
                            'type': 'input_image',
                            'image_url': f"data:image/jpeg;base64,{image_base64}"
                        }
                    ]
                }
            ]
        )
        text = response.output_text
        logger.info(f"Texto extraído por OpenAI: {text}")
        
        return text
    except Exception as e:
        logger.error(f"Error al contactar con OpenAI: {e}")
        return None

def save_image_to_cache(image_bytes: bytes, text: str) -> None:
    """
    Guarda el hash de la imagen y el texto extraído en el caché.
    """
    image_hash = hashlib.sha256(image_bytes).hexdigest()
    LAST_MESSAGES_CACHE.append((image_hash, text))
    logger.info(f"Imagen guardada en caché con texto: {text}")
