from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__, template_folder="../frontend/templates")
    CORS(app)
    
    app.config["SECRET_KEY"] = os.getenv("secret_key")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    
    db.init_app(app)
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    
    from .models import User, Task
    
    if not os.path.exists( "/backend" + DB_NAME):
        with app.app_context():
            db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app
    
    
    
