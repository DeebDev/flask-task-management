import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, url_for
from markupsafe import escape
from routes.PriorityRoutes import priority_bp
from routes.TaskRoutes import task_bp
from routes.UserRoutes import user_bp
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models.User import User
from models.Task import Task
from models.Priority import Priority
from db import db

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db.init_app(app)

app.register_blueprint(priority_bp)
app.register_blueprint(task_bp)
app.register_blueprint(user_bp)

with app.app_context():
    db.drop_all()
    db.create_all()
    priority1 = Priority.query.filter_by(name='High Priority').first()
    if not priority1:
        priority1 = Priority(name='High Priority', due_date_within=1)
        db.session.add(priority1)
    priority2 = Priority.query.filter_by(name='Medium Priority').first()
    if not priority2:
        priority2 = Priority(name='Medium Priority', due_date_within=3)
        db.session.add(priority2)
    db.session.commit()


admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Task, db.session))
admin.add_view(ModelView(Priority, db.session))

@app.route("/")
def home():
    return "Welcome, Your in home screen."

