import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuración para evitar problemas con Bandit"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave-secreta-para-el-tp-2026')
    
    # Importante: nunca hardcodear debug=True
    DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    @staticmethod
    def get_db_url():
        """Convierte postgres:// a postgresql:// si es necesario (Render usa postgres://)"""
        url = os.getenv('DATABASE_URL')
        if url and url.startswith('postgres://'):
            url = url.replace('postgres://', 'postgresql://', 1)
        return url