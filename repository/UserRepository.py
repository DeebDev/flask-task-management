from db import db
from sqlalchemy.exc import SQLAlchemyError
from  werkzeug.security import check_password_hash
from models.User import User

def get_users():
    users = User.query.all()
    user_list = []
    for user in users:
        tasks = [{'id': task.id, 'name': task.name, 'description': task.description} for task in user.tasks]
        user_list.append({'id': user.id, 'name': user.name, 'email': user.email, 'tasks': tasks})
    return user_list

def login_user(email, password):
    current_user = User.query.filter_by(email=email).first()
    if not current_user:
        return None
    if check_password_hash(current_user.password, password):
        return current_user
    return None

def create_user(name, email, password):
    user = User.query.filter_by(email=email).first()
    if user:
        return None
    try:
        user = User(name, email, password)
        db.session.add(user)
        db.session.commit()
        return user
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Database error occurred: {e}")
        return None

