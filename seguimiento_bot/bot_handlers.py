from telegram import Update, File
from telegram.ext import ContextTypes

from .config import logger
from .image_processor import extract_text_from_image
from .web_scraper import get_tracking_data
from .data_processor import process_tracking_data

async def _get_and_send_tracking_info(update: Update, tracking_number: str) -> None:
    """Helper function to get and send tracking information."""
    await update.message.reply_text(tracking_number)

    try:
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
        logger.error(f"Error in _get_and_send_tracking_info: {e}")
        await update.message.reply_text("Ocurrió un error inesperado al procesar tu solicitud.")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler para el comando /start."""
    await update.message.reply_text(
        "¡Hola! Envíame una foto con un número de guía de Vía Cargo o el número de 12 dígitos y te daré el estado del envío."
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles text messages, checking for a 12-digit tracking number."""
    if not update.message or not update.message.text:
        return

    message_text = update.message.text.strip()
    if message_text.isdigit() and len(message_text) == 12:
        await _get_and_send_tracking_info(update, message_text)
    else:
        await update.message.reply_text("No parece un número de seguimiento válido. Por favor, envía una foto con el número de guía o un número de 12 dígitos.")


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

        tracking_number = await extract_text_from_image(image_bytes)
        if not tracking_number:
            await update.message.reply_text("No pude extraer un número de seguimiento de la imagen. Intenta con una foto más clara.")
            return

        await _get_and_send_tracking_info(update, tracking_number)

    except Exception as e:
        logger.error(f"Error en handle_image: {e}")
        await update.message.reply_text("Ocurrió un error inesperado al procesar tu solicitud.")