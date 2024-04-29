from json import dump
from flask import Blueprint, jsonify, request, make_response
import jwt
import os
from dotenv import load_dotenv
from functools import wraps
from models.User import User
from  werkzeug.security import generate_password_hash, check_password_hash
from services.UserService import get_users_service, create_user_service, login_user_service
from datetime import datetime, timedelta

user_bp = Blueprint('users', __name__)

load_dotenv()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['id']).first()
        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)
    return decorated

@user_bp.route('/api/v1/users', methods=['GET'])
@token_required
def get_users(current_user):
    users = get_users_service()
    user_list = [{'id': user['id'], 'name': user['name'], 'email': user['email'], 'tasks': user['tasks']} for user in users]
    return jsonify({'users': user_list}), 200

@user_bp.route('/api/v1/login', methods=['POST'])
def login():
    auth = request.json
    if not auth or not auth.get('email') or not auth.get('password'):
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required !!"'})
    try:
        current_user = login_user_service(auth.get('email'), auth.get('password'))
        if not current_user:
            return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="User does not exist !!"'})
        token = jwt.encode({'id': current_user.id}, os.getenv('SECRET_KEY'))
        return jsonify({'message': 'Logged in successfully', 'token': token}), 201
    except Exception as e:
        print(f"An error occurred: {e}")
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="{e}"'})

@user_bp.route('/api/v1/signup', methods=['POST'])
def signup():
    data = request.json

    if not data or not data.get('name') or not data.get('email') or not data.get('password'):
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="All fields are required !!"'})

    name, email = data.get('name'), data.get('email')
    password = generate_password_hash(data.get('password'))

    user = create_user_service(name, email, password)
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="User already exists!!"'})
    token = jwt.encode({'id': user.id}, os.getenv('SECRET_KEY'))
    return jsonify({'message': 'Successfully registered', 'token': token}), 201
