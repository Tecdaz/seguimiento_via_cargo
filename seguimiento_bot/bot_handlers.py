from telegram import Update, File
from telegram.ext import ContextTypes

from .config import logger
from .image_processor import extract_text_from_image
from .web_scraper import get_tracking_data
from .data_processor import process_tracking_data

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler para el comando /start."""
    await update.message.reply_text(
        "¡Hola! Envíame una foto con un número de guía de Vía Cargo y te daré el estado del envío."
    )

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Procesa la imagen recibida, extrae el texto y busca la información de seguimiento.
    """
    if not update.message or not update.message.photo:
        return

    await update.message.reply_text("Procesando imagen...")

    try:
        photo_file: File = await context.bot.get_file(update.message.photo[-1].file_id)
        image_bytes = await photo_file.download_as_bytearray()

        # 1. Extraer texto de la imagen
        tracking_number = await extract_text_from_image(bytes(image_bytes))
        if not tracking_number:
            await update.message.reply_text("No pude extraer un número de seguimiento de la imagen. Intenta con una foto más clara.")
            return

        await update.message.reply_text(f"Número de guía detectado: {tracking_number}. Buscando información...")

        # 2. Obtener datos de seguimiento con Playwright
        tracking_data = await get_tracking_data(tracking_number)
        if not tracking_data:
            await update.message.reply_text("No pude obtener la información de seguimiento. Es posible que el número no sea válido o que el servicio no esté disponible.")
            return
            
        # 3. Procesar y formatear los datos para el usuario
        user_message = process_tracking_data(tracking_data)
        
        # 4. Enviar resultado al usuario
        await update.message.reply_text(user_message)

    except Exception as e:
        logger.error(f"Error en handle_image: {e}")
        await update.message.reply_text("Ocurrió un error inesperado al procesar tu solicitud.")
