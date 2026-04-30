from datetime import datetime

from flask import Blueprint, jsonify, request
from app import db
from app.models import User

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/health', methods=['GET'])
def health():
    """Endpoint de healthcheck (obligatorio)"""
    return jsonify({
        "status": "healthy",
        "message": "API IAS - Trabajo Práctico funcionando correctamente"
    }), 200

@bp.route('/users', methods=['GET'])
def get_users():
    """Obtener todos los usuarios"""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

@bp.route('/users', methods=['POST'])
def create_user():
    """Crear un nuevo usuario"""
    data = request.get_json()
    if not data or not data.get('first_name') or not data.get('last_name') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Faltan datos: first_name, last_name, email y password son requeridos"}), 400

    birthdate = None
    if data.get('birthdate'):
        try:
            birthdate = datetime.fromisoformat(data['birthdate']).date()
        except ValueError:
            return jsonify({"error": "Formato de birthdate inválido. Use YYYY-MM-DD."}), 400

    user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password=data['password'],
        birthdate=birthdate
    )
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user.to_dict()), 201