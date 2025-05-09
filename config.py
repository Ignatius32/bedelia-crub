import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-insegura')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True
