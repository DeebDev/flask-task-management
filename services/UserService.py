from repository.UserRepository import get_users, login_user, create_user

def get_users_service():
    return get_users()

def login_user_service(email, password):
    return login_user(email, password)

def create_user_service(name, email, password):
    return create_user(name, email, password)