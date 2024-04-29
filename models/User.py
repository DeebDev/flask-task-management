from db import db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(225))
    tasks = db.relationship('Task', backref='user', lazy=True)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
