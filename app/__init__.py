from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configuración de la base de datos
    db_url = Config.get_db_url()
    if db_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    else:
        # Para testing local (SQLite)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    db.init_app(app)
    
    # Registrar rutas
    from app.routes import bp as api_bp
    app.register_blueprint(api_bp)
    
    return app