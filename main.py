from telegram.ext import Application, CommandHandler, MessageHandler, filters

from seguimiento_bot.config import TELEGRAM_TOKEN, OPENAI_API_KEY, logger
from seguimiento_bot.bot_handlers import start, handle_image

def main() -> None:
    """Inicia el bot de Telegram."""
    if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
        logger.critical("Faltan las variables de entorno TELEGRAM_TOKEN u OPENAI_API_KEY. El bot no puede iniciar.")
        return

    logger.info("Iniciando bot...")
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_image))

    # Iniciar el bot
    application.run_polling()


if __name__ == "__main__":
    main()
