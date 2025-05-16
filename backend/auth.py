from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import login_required, logout_user, login_user, current_user
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = User.query.get(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash("Logged in successfully", category="success")
                return redirect(url_for("views.home"))
            else:
                flash("Password incorrect", category="error")
        else:
            flash("User cannot be found", category="error")
        
    return render_template("login.html", user=current_user)

@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        # Recieve input from submitted form
        email = request.form.get("email")
        first_name = request.form.get("firstName")
        password = request.form.get("password")
        password2 = request.form.get("password2")
        
        # Check all data from form is valid
        if not email_is_valid(email):
            flash("Invalid email submitted", category="error")
        elif len(password) < 8:
            flash("Password is too short", category="error") 
        elif password != password2:
            flash("Passwords don't match", category="error")
        elif len(first_name) < 2:
            flash("Name is too short", category="error")
        else:
            first_name = sanatize_input(first_name)
            password = generate_password_hash(password, "pbkdf2:sha256", salt_length=16)
            
            # Create new user and add to the database
            new_user = User(email=email, first_name=first_name, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash("Sign up successful", category="success")
            
            # Redirect to the home page as logged in after signup
            user = User.query.get(email=email).first()
            return redirect(url_for("views.home"))
        
    return render_template("signUp.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out", category="success")
    
    return redirect(url_for("auth.login"))



def email_is_valid(email):
    # Check for valid email
    return True

def sanatize_input(input):
    return input