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

@bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Actualizar un usuario existente"""
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se enviaron datos para actualizar"}), 400
    
    allowed_fields = {'first_name', 'last_name', 'email', 'password', 'birthdate'}
    if not any(field in data for field in allowed_fields):
        return jsonify({"error": "No se enviaron campos válidos para actualizar"}), 400
    
    if 'first_name' in data:
        if not data['first_name']:
            return jsonify({"error": "first_name no puede estar vacío"}), 400
        user.first_name = data['first_name']
    if 'last_name' in data:
        if not data['last_name']:
            return jsonify({"error": "last_name no puede estar vacío"}), 400
        user.last_name = data['last_name']
    if 'email' in data:
        if not data['email']:
            return jsonify({"error": "email no puede estar vacío"}), 400
        existing = User.query.filter_by(email=data['email']).first()
        if existing and existing.id != user_id:
            return jsonify({"error": "Ya existe otro usuario con ese email"}), 409
        user.email = data['email']
    if 'password' in data:
        if not data['password']:
            return jsonify({"error": "password no puede estar vacío"}), 400
        user.password = data['password']
    if 'birthdate' in data:
        if data['birthdate'] is None or data['birthdate'] == '':
            user.birthdate = None
        else:
            try:
                user.birthdate = datetime.fromisoformat(data['birthdate']).date()
            except ValueError:
                return jsonify({"error": "Formato de birthdate inválido. Use YYYY-MM-DD."}), 400
    
    db.session.commit()
    return jsonify(user.to_dict()), 200


@bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Eliminar un usuario"""
    user = User.query.get_or_404(user_id)
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({
        "message": f"Usuario con ID {user_id} eliminado correctamente"
    }), 200