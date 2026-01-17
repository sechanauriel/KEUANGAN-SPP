# app/routes/__init__.py
from flask import Blueprint
from .billing_routes import billing_bp
from .payment_routes import payment_bp
from .dashboard_routes import dashboard_bp
from .webhook_routes import webhook_bp
from .student_routes import student_bp

def register_routes(app):
    """Register all routes to Flask app"""
    app.register_blueprint(billing_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(webhook_bp)
    app.register_blueprint(student_bp)
