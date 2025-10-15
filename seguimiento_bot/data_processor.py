from datetime import datetime
from .config import logger

def process_tracking_data(tracking_data: dict) -> str | None:
    """
    Procesa los datos de seguimiento para encontrar el evento más reciente
    y devuelve una cadena de texto formateada con la información relevante.
    """
    try:
        # 1. Acceder a la lista de eventos de forma segura
        events = tracking_data.get('ok', [{}])[0].get('objeto', {}).get('listaEventos', [])
        
        if not events:
            logger.warning("No se encontraron eventos en los datos de seguimiento.")
            return "No se encontraron eventos para este envío."

        # 2. Encontrar el evento más reciente
        # El formato de fecha es "DD/MM/YYYY HH:MM"
        latest_event = max(events, key=lambda event: datetime.strptime(event['fechaEvento'], "%d/%m/%Y %H:%M"))

        # 3. Extraer la información requerida
        descripcion = latest_event.get('descripcion', 'N/A')
        dele_nombre = latest_event.get('deleNombre', 'N/A')
        fecha_evento = latest_event.get('fechaEvento', 'N/A')

        # 4. Formatear la salida para el usuario
        return (
            f"Último Estado del Envío:\n\n"
            f"Descripción: {descripcion}\n"
            f"Lugar: {dele_nombre}\n"
            f"Fecha: {fecha_evento}"
        )

    except (IndexError, KeyError, TypeError, ValueError) as e:
        logger.error(f"Error al procesar los datos de seguimiento: {e}")
        logger.debug(f"Datos recibidos que causaron el error: {tracking_data}")
        return "No se pudo procesar la respuesta del servicio de seguimiento. El formato puede haber cambiado."
