import base64
from .config import client, logger

async def extract_text_from_image(image_bytes: bytes) -> str | None:
    """
    Envía una imagen a la API de OpenAI Vision para extraer texto.
    """
    if not client:
        logger.error("Cliente de OpenAI no inicializado. Verifica la API key.")
        return None
    
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
