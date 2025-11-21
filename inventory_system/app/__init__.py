from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
import os  # Add this import

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    
    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except Exception as e:
        print(f"Error creating instance folder: {e}")
    
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    from app.employee import bp as employee_bp
    app.register_blueprint(employee_bp, url_prefix='/employee')
    
    @app.route('/')
    def index():
        from flask import redirect, url_for
        return redirect(url_for('auth.login'))
    
    return app