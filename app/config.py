import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuración para evitar problemas con Bandit"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave-secreta-para-el-tp-2026')
    
    # Importante: nunca hardcodear debug=True
    DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Opciones de conexión para psycopg3
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
    }
    
    @staticmethod
    def get_db_url():
        # """Convierte postgres:// a postgresql+psycopg:// para usar psycopg3"""
        url = os.getenv('DATABASE_URL')
        # if url:
        #     # Reemplazar el driver para usar psycopg3
        #     if url.startswith('postgres://'):
        #         url = url.replace('postgres://', 'postgresql+psycopg://', 1)
        #     elif url.startswith('postgresql://'):
        #         url = url.replace('postgresql://', 'postgresql+psycopg://', 1)
        return url