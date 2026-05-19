import logging
import requests
from ..constants import API_BASE_URL

logger = logging.getLogger(__name__)


def obtener_mascotas_disponibles() -> list[dict]:
    """Consume el endpoint del backend para obtener las mascotas disponibles para adopcion."""
    try:
        response = requests.get(f'{API_BASE_URL}/mascotas/disponibles', timeout=10)

        if response.status_code == 204:
            return []

        if response.status_code == 200:
            data = response.json()

            return data.get('mascotas', [])

        logger.error(f"Error al obtener mascotas: HTTP {response.status_code}")

        return []

    except requests.exceptions.ConnectionError:
        logger.error(f"No se pudo conectar con la API en {API_BASE_URL}")

        return []

    except requests.exceptions.Timeout:
        logger.error("Timeout al conectar con la API")

        return []

    except Exception as e:
        logger.error(f"Error inesperado al obtener mascotas: {e}")

        return []


def obtener_mascota_por_id(id_mascota: int) -> dict:
    """Consume el endpoint del backend para obtener una mascota por id."""
    try:
        response = requests.get(f'{API_BASE_URL}/mascotas/{id_mascota}', timeout=10)

        if response.status_code == 200:
            return response.json()

        return {}

    except Exception as e:
        logger.error(f"Error al obtener mascota {id_mascota}: {e}")

        return {}


def crear_mascota(form_data: dict, archivo) -> dict:
    """
    Envia los datos del formulario y la imagen al backend via multipart/form-data.
    Retorna el dict de la mascota creada, o un dict con 'errores' si falla.
    """
    try:
        files = {}

        if archivo and archivo.filename:
            files['imagen'] = (archivo.filename, archivo.stream, archivo.content_type)

        response = requests.post(
            f'{API_BASE_URL}/mascotas',
            data=form_data,
            files=files,
            timeout=30
        )

        if response.status_code == 201:
            return response.json()

        # Intentar extraer errores del backend
        try:
            error_data = response.json()
            errores = error_data.get('errors', [])
            mensajes = [e.get('description', e.get('message', 'Error desconocido')) for e in errores]
            
            return {'errores': mensajes}
        except Exception:
            return {'errores': [f'Error del servidor: HTTP {response.status_code}']}

    except requests.exceptions.ConnectionError:
        logger.error(f"No se pudo conectar con la API en {API_BASE_URL}")

        return {'errores': ['No se pudo conectar con el servidor. Verifica que la API este corriendo.']}

    except requests.exceptions.Timeout:
        logger.error("Timeout al enviar mascota a la API")

        return {'errores': ['La solicitud tardo demasiado. Intenta nuevamente.']}

    except Exception as e:
        logger.error(f"Error inesperado al crear mascota: {e}")

        return {'errores': [f'Error inesperado: {e}']}
