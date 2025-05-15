from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from .models import User

load_dotenv()
db = SQLAlchemy()
DB_NAME = "database"

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    app.config["SECRET_KEY"] = os.getenv("secret_key")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}.db"
    
    db.init_app()
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, "/views")
    app.register_blueprint(auth, "/auth")
    

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app()
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app
    
    
    
