from db import db

class Priority(db.Model):
    __tablename__ = 'proirities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    due_date_within = db.Column(db.Integer, nullable=False)
    tasks = db.relationship('Task', backref='priority', lazy=True)
    def __init__(self, name, due_date_within):
        self.name = name
        self.due_date_within = due_date_within