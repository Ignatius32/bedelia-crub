import requests
from requests.auth import HTTPDigestAuth
from functools import lru_cache
import logging

# Configuración básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MateriaService:
    """Servicio para interactuar con la API de materias"""
    
    BASE_URL = "https://huayca.crub.uncoma.edu.ar/catedras/1.0/rest"
    def __init__(self, username="usuario1", password="pdf"):
        self.username = username
        self.password = password
        self.session = requests.Session()
        # Usar autenticación Digest en lugar de Basic
        self.session.auth = requests.auth.HTTPDigestAuth(self.username, self.password)
    
    @lru_cache(maxsize=128)
    def get_materias(self):
        """
        Obtiene todas las materias desde la API.
        Utiliza cache para evitar múltiples llamadas innecesarias.
        """
        try:
            response = self.session.get(f"{self.BASE_URL}/materias")
            response.raise_for_status()  # Lanza una excepción para códigos de estado HTTP erróneos
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al obtener materias: {e}")
            return []
    
    def get_materia_by_id(self, id_materia):
        """Obtiene una materia específica por su ID"""
        try:
            response = self.session.get(f"{self.BASE_URL}/materias/{id_materia}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al obtener materia con ID {id_materia}: {e}")
            return None
    def search_materias(self, query):
        """Busca materias que coincidan con la consulta en el nombre"""
        try:
            # Usar el endpoint específico de búsqueda por nombre_materia
            response = self.session.get(f"{self.BASE_URL}/materias", params={"nombre_materia": query})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al buscar materias: {e}")
            return []

# Crear una instancia del servicio para uso general
materia_service = MateriaService()
