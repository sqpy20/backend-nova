from flask import Flask
from flask_cors import CORS
from config import Config
from .extensions import db, jwt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    CORS(app)
    db.init_app(app)
    jwt.init_app(app)
    
    # Import and register blueprints
    from .admin_routes import admin_bp
    from .student_routes import student_bp
    app.register_blueprint(admin_bp)
    app.register_blueprint(student_bp)
    
    return app