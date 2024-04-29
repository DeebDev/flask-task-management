from db import db

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    priority_id = db.Column(db.Integer, db.ForeignKey('proirities.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, name, description, priority_id, user_id, completed):
        self.name = name
        self.description = description
        self.priority_id = priority_id
        self.user_id = user_id
        self.completed = completed

    def json(self):
        return {'id': self.id, 'name': self.name, 'description': self.description, 'priority_id': self.priority_id, 'user_id': self.user_id, 'completed': self.completed}
