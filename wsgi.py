"""WSGI config for the application."""
from app import create_app, db

app = create_app()

# Crear tablas si no existen
with app.app_context():
    db.create_all()