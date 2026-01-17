# app/__init__.py
import os
from flask import Flask
from flask_cors import CORS
from app.config import config
from app.models import db

def create_app(config_name='development'):
    """Application factory"""
    # Get the directory of the app module
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
    
    app = Flask(__name__, template_folder=template_dir)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Register blueprints
    from app.routes import register_routes
    register_routes(app)
    
    # Setup scheduler
    from app.schedulers import setup_billing_scheduler
    with app.app_context():
        setup_billing_scheduler(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found'}, 404
    
    @app.errorhandler(500)
    def server_error(error):
        return {'error': 'Server error'}, 500
    
    return app
