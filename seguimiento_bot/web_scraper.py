import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from .config import logger

async def get_tracking_data(tracking_number: str) -> dict | None:
    """
    Navega a la página de seguimiento con Playwright y captura los datos del envío
    escuchando las respuestas de la red.
    """
    logger.info(f"Iniciando Playwright para el número de seguimiento: {tracking_number}")
    
    API_URL_SUBSTRING = "ws.busplus.com.ar/alerce/tracking"
    TRACKING_PAGE_URL = f"https://www.viacargo.com.ar/tracking/{tracking_number}"

    captured_data = None

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Usamos un asyncio.Future para esperar de forma asíncrona los datos de la respuesta
        response_future = asyncio.Future()

        async def on_response(response):
            # Verificamos si la URL de la respuesta es la que buscamos
            if API_URL_SUBSTRING in response.url and response.ok:
                try:
                    data = await response.json()
                    logger.info("Datos JSON de la respuesta capturados.")
                    # Asignamos el resultado al Future si aún no se ha completado
                    if not response_future.done():
                        response_future.set_result(data)
                except Exception as e:
                    logger.error(f"Error al procesar JSON de la respuesta: {e}")
                    if not response_future.done():
                        response_future.set_exception(e)

        # Registramos el listener para el evento 'response'
        page.on("response", on_response)

        try:
            logger.info(f"Navegando a: {TRACKING_PAGE_URL}")
            await page.goto(TRACKING_PAGE_URL, wait_until="networkidle")

            # Esperamos a que el Future se complete (con un timeout de 15s)
            captured_data = await asyncio.wait_for(response_future, timeout=15.0)

        except asyncio.TimeoutError:
            logger.warning("Timeout: No se recibió la respuesta de la API a tiempo.")
        except Exception as e:
            logger.error(f"Error durante la ejecución de Playwright: {e}")
        finally:
            await browser.close()
            logger.info("Navegador Playwright cerrado.")

    return captured_data
