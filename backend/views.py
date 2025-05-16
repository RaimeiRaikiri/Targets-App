from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import User, Task
from . import db
from os import path

views = Blueprint("views", __name__)

@views.route("/tasks", methods=["GET", "POST"])
@login_required
def tasks():
    if request.method == "POST":
        # Get task input data
        task_content = request.form.get("task_content")
        deadline = request.form.get("deadline")
        
        # Sanatize it 
        task_content = sanatize_input(task_content)
        
        # Check if there is task content
        if len(task_content) < 1:
            flash()
        else:
            new_task = Task(task_content=task_content, deadline=deadline, user_id=current_user.id)
            db.session.add(new_task)
            db.session.commit()
            flash("New task added")
        
    return render_template("tasks.html", user=current_user)

@views.route("/home")
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route("/")
def landing_page():
    return render_template("base.html", user=current_user)

def sanatize_input(input):
    return input