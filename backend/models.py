from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    first_name = db.Column(db.String(120), nullable=False, unique=False)
    password = db.Column(db.String(120), nullable=False, unique=False)
    tasks = db.relationship("Task")
    
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_content = db.Column(db.String(5000), nullable=False, unique=False)
    create_date = db.Column(db.Date)
    deadline = db.Column(db.Date, nullable=True)
    complete_status = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))