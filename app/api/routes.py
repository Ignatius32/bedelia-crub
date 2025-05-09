from flask import Blueprint, jsonify, request
from app.services.api import materia_service

api = Blueprint('api', __name__)

@api.route('/materias', methods=['GET'])
def get_materias():
    """Endpoint para obtener todas las materias"""
    materias = materia_service.get_materias()
    return jsonify(materias)

@api.route('/materias/<int:id_materia>', methods=['GET'])
def get_materia(id_materia):
    """Endpoint para obtener una materia por su ID"""
    materia = materia_service.get_materia_by_id(id_materia)
    if materia:
        return jsonify(materia)
    return jsonify({"error": "Materia no encontrada"}), 404

@api.route('/materias/search', methods=['GET'])
def search_materias():
    """Endpoint para buscar materias por nombre"""
    query = request.args.get('q', '')
    if not query or len(query) < 3:
        return jsonify([])
    
    materias = materia_service.search_materias(query)
    return jsonify(materias)
