from db import db
from models.Task import Task

def get_tasks():
    tasks = db.session.query(Task).all()
    return tasks

def get_task_by_id(id):
    task = db.session.query(Task).filter_by(id=id).first()
    if task is None:
        return None
    return task

def get_tasks_by_user_id(user_id):
    tasks = db.session.query(Task).filter_by(user_id=user_id).all()
    return tasks

def get_completed_tasks():
    tasks = db.session.query(Task).filter_by(completed=True).all()
    return tasks

def get_incomplete_tasks():
    tasks = db.session.query(Task).filter_by(completed=False).all()
    return tasks

def create_task(title, description, priority_id, user_id, completed=False):
    task = Task(title, description, priority_id, user_id, completed)
    db.session.add(task)
    db.session.commit()
    return task

def update_task(id, title, description, priority_id, user_id, completed=False):
    task = db.session.query(Task).filter_by(id=id).first()
    if task is None:
        return None
    task.title = title
    task.description = description
    task.priority_id = priority_id
    task.user_id = user_id
    task.completed = completed
    db.session.commit()
    return task

def complete_task(id):
    task = db.session.query(Task).filter_by(id=id).first()
    if task is None:
        return None
    task.completed = True
    db.session.commit()
    return task

def incomplete_task(id):
    task = db.session.query(Task).filter_by(id=id).first()
    if task is None:
        return None
    task.completed = False
    db.session.commit()
    return task

def delete_task_api(id):
    task = db.session.query(Task).filter_by(id=id).first()
    if task is None:
        return None
    db.session.delete(task)
    db.session.commit()
    return task

