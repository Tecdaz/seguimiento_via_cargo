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
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    
    try:
        response = await client.chat.completions.create(
            model="gpt-4.1-nano-2025-04-14",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extrae el número de seguimiento o guía de esta imagen. Devuelve únicamente el número, sin texto adicional."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=100,
        )
        text = response.choices[0].message.content.strip()
        logger.info(f"Texto extraído por OpenAI: {text}")
        return text
    except Exception as e:
        logger.error(f"Error al contactar con OpenAI: {e}")
        return None
