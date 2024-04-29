from flask import Blueprint, jsonify, request
from services.PriorityService import get_priorities_service, get_priority_by_id_service, create_priority_service, update_priority_service, delete_priority_service
from routes.UserRoutes import token_required

priority_bp = Blueprint('priorities', __name__)

@priority_bp.route('/api/v1/priorities', methods=['GET'])
def get_priorities():
    priorities = get_priorities_service()
    priorities_list = [{'id': priority.id, 'name': priority.name, 'due_date_within': priority.due_date_within} for priority in priorities]
    return jsonify({'priorities': priorities_list}), 200


@priority_bp.route('/api/v1/priorities/<int:id>', methods=['GET'])
def get_priority_by_id(id):
    priority = get_priority_by_id_service(id)
    if priority is None:
        return jsonify({'error': 'Priority not found'}), 404
    return jsonify({'id': priority.id, 'name': priority.name, 'due_date_within': priority.due_date_within}), 200


@priority_bp.route('/api/v1/priorities', methods=['POST'])
def create_priority():
    if 'name' not in request.json or 'due_date_within' not in request.json:
        return jsonify({'error': 'Missing name or due_date_within'}), 400

    name = request.json['name']
    due_date_within = request.json['due_date_within']

    if not name or type(name) != str:
        return jsonify({'error': 'Invalid name'}), 400
    if not isinstance(due_date_within, int) or due_date_within <= 0:
        return jsonify({'error': 'Invalid due_date_within'}), 400

    new_priority_id = create_priority_service(name, due_date_within)
    return jsonify({'message': 'Priority Created Successfully', 'id': new_priority_id}), 201


@priority_bp.route('/api/v1/priorities/<int:id>', methods=['PUT'])
def update_priority(id):
    if 'name' not in request.json or 'due_date_within' not in request.json:
        return jsonify({'error': 'Missing name or due_date_within'}), 400

    name = request.json['name']
    due_date_within = request.json['due_date_within']

    if not name or type(name) != str:
        return jsonify({'error': 'Invalid name'}), 400
    if not isinstance(due_date_within, int) or due_date_within <= 0:
        return jsonify({'error': 'Invalid due_date_within'}), 400

    priority = get_priority_by_id_service(id)
    if priority is None:
        return jsonify({'error': 'Priority not found'}), 404
    else:
        update_priority_service(id, name, due_date_within)
    return jsonify({'message': 'Priority Updated Successfully', 'id': id}), 200


@priority_bp.route('/api/v1/priorities/<int:id>', methods=['DELETE'])
def delete_priority(id):
    priority = get_priority_by_id_service(id)
    if priority is None:
        return jsonify({'error': 'Priority not found'}), 404
    else:
        delete_priority_service(id)
    return jsonify({'message': 'Priority Deleted Successfully'}), 200