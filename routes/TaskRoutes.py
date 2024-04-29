from flask import Blueprint, jsonify, request
from db import db
from repository.TaskRepository import get_tasks, get_task_by_id, delete_task_api, create_task, update_task, get_tasks_by_user_id, complete_task, incomplete_task, get_completed_tasks, get_incomplete_tasks
from routes.UserRoutes import token_required
from models.User import User
from models.Priority import Priority

task_bp = Blueprint('tasks', __name__)

@task_bp.route('/api/v1/tasks', methods=['GET'])
def get_tasks_fucntion():
    tasks = get_tasks()
    tasks_list = []
    for task in tasks:
        user = db.session.query(User).filter_by(id=task.user_id).first()
        priority = db.session.query(Priority).filter_by(id=task.priority_id).first()
        tasks_list.append({'id': task.id, 'name': task.name, 'description': task.description, 'completed': task.completed, 'priority': {"name": priority.name, 'due_date_within(days)': priority.due_date_within}, 'user': user.name})

    return jsonify({'tasks': tasks_list}), 200

@task_bp.route('/api/v1/tasks/<int:id>', methods=['Get'])
def get_task_by_id_function(id):
    task = get_task_by_id(id)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    user = db.session.query(User).filter_by(id=task.user_id).first()
    priority = db.session.query(Priority).filter_by(id=task.priority_id).first()
    return jsonify({'id': task.id, 'name': task.name, 'description': task.description, 'completed': task.completed, 'priority': {"name": priority.name, 'due_date_within(days)': priority.due_date_within}, 'user': user.name}), 200

@task_bp.route('/api/v1/user/tasks', methods=['GET'])
@token_required
def get_user_tasks(current_user):
    if not current_user:
        return jsonify({'error': 'Unauthenticated !!'}), 401
    id = current_user.id
    tasks = get_tasks_by_user_id(id)
    tasks_list = []
    for task in tasks:
        user = db.session.query(User).filter_by(id=task.user_id).first()
        priority = db.session.query(Priority).filter_by(id=task.priority_id).first()
        tasks_list.append({'id': task.id, 'name': task.name, 'description': task.description, 'completed': task.completed, 'priority': {"name": priority.name, 'due_date_within(days)': priority.due_date_within}, 'user': user.name})

    return jsonify({'tasks': tasks_list}), 200

@task_bp.route('/api/v1/tasks', methods=['POST'])
@token_required
def create_task_function(current_user):
    if not current_user:
        return jsonify({'error': 'Unauthenticated !!'}), 401

    if 'name' not in request.json or 'description' not in request.json or 'priority_id' not in request.json:
        return jsonify({'error': 'Missing name, description, or priority_id'}), 400

    name = request.json['name']
    description = request.json['description']
    priority_id = request.json['priority_id']
    user_id = current_user.id

    if not name or type(name) != str:
        return jsonify({'error': 'Invalid name'}), 400
    if not description or type(description) != str:
        return jsonify({'error': 'Invalid description'}), 400
    if not isinstance(priority_id, int) or priority_id <= 0:
        return jsonify({'error': 'Invalid priority_id'}), 400

    new_task_id = create_task(name, description, priority_id, user_id, False)
    return jsonify({'message': 'Task Created Successfully', 'id': new_task_id.id}), 201

@task_bp.route('/api/v1/tasks/<int:id>', methods=['PUT'])
@token_required
def update_task_function(current_user, id):
    if not current_user:
        return jsonify({'error': 'Unauthenticated !!'}), 401

    if 'name' not in request.json or 'description' not in request.json or 'priority_id' not in request.json:
        return jsonify({'error': 'Missing name, description, or priority_id'}), 400

    name = request.json['name']
    description = request.json['description']
    priority_id = request.json['priority_id']
    completed = request.json['completed']
    user_id = current_user.id

    if not name or type(name) != str:
        return jsonify({'error': 'Invalid name'}), 400
    if not description or type(description) != str:
        return jsonify({'error': 'Invalid description'}), 400
    if not isinstance(priority_id, int) or priority_id <= 0:
        return jsonify({'error': 'Invalid priority_id'}), 400
    if not isinstance(completed, bool):
        return jsonify({'error': 'Invalid completed'}), 400

    task = get_task_by_id(id)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    else:
        if user_id!= task.user_id:
            return jsonify({'error': 'You do not have permission to update this task'}), 401

        update_task(id, name, description, priority_id, user_id, completed)
        return jsonify({'message': 'Task Updated Successfully', 'id': id}), 200

@task_bp.route('/api/v1/tasks/<int:id>', methods=['DELETE'])
@token_required
def delete_task_function(current_user, id):
    task = get_task_by_id(id)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    else:
        if current_user.id!= task.user_id:
            return jsonify({'error': 'You do not have permission to delete this task'}), 401
        delete_task_api(id)
    return jsonify({'message': 'Task Deleted Successfully'}), 200

@task_bp.route('/api/v1/tasks/completed', methods=['GET'])
@token_required
def get_completed_tasks_function(current_user):
    if not current_user:
        return jsonify({'error': 'Unauthenticated !!'}), 401
    tasks = get_completed_tasks()
    tasks_list = []
    for task in tasks:
        user = db.session.query(User).filter_by(id=task.user_id).first()
        priority = db.session.query(Priority).filter_by(id=task.priority_id).first()
        tasks_list.append({'id': task.id, 'name': task.name, 'description': task.description, 'completed': task.completed, 'priority': {"name": priority.name, 'due_date_within(days)': priority.due_date_within}, 'user': user.name})

    return jsonify({'tasks': tasks_list}), 200


@task_bp.route('/api/v1/tasks/incomplete', methods=['GET'])
@token_required
def get_incomplete_tasks_function(current_user):
    if not current_user:
        return jsonify({'error': 'Unauthenticated !!'}), 401
    tasks = get_incomplete_tasks()
    tasks_list = []
    for task in tasks:
        user = db.session.query(User).filter_by(id=task.user_id).first()
        priority = db.session.query(Priority).filter_by(id=task.priority_id).first()
        tasks_list.append({'id': task.id, 'name': task.name, 'description': task.description, 'completed': task.completed, 'priority': {"name": priority.name, 'due_date_within(days)': priority.due_date_within}, 'user': user.name})

    return jsonify({'tasks': tasks_list}), 200

    if not current_user:
        return jsonify({'error': 'Unauthenticated !!'}), 401
    tasks = get_incomplete_tasks()
    tasks_list = []
    for task in tasks:
        user = db.session.query(User).filter_by(id=task.user_id).first()
        priority = db.session.query(Priority).filter_by(id=task.priority_id).first()
        tasks_list.append({'id': task.id, 'name': task.name, 'description': task.description, 'completed': task.completed, 'priority': {"name": priority.name, 'due_date_within(days)': priority.due_date_within}, 'user': user.name})

    return jsonify({'tasks': tasks_list}), 200

@task_bp.route('/api/v1/tasks/<int:id>/completed', methods=['PUT'])
@token_required
def complete_task_function(current_user, id):
    if not current_user:
        return jsonify({'error': 'Unauthenticated !!'}), 401

    task = get_task_by_id(id)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    if current_user.id!= task.user_id:
        return jsonify({'error': 'You do not have permission to complete this task'}), 401
    task = complete_task(id)
    return jsonify({'message': 'Task Completed Successfully', 'id': id}), 200

@task_bp.route('/api/v1/tasks/<int:id>/incomplete', methods=['PUT'])
@token_required
def incomplete_task_function(current_user, id):
    if not current_user:
        return jsonify({'error': 'Unauthenticated !!'}), 401

    task = get_task_by_id(id)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    if current_user.id!= task.user_id:
        return jsonify({'error': 'You do not have permission to incomplete this task'}), 401
    task = incomplete_task(id)
    return jsonify({'message': 'Task Incomplete Successfully', 'id': id}), 200