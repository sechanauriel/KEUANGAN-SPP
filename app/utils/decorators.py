# app/utils/decorators.py
from functools import wraps
from flask import request, jsonify

def jwt_required(f):
    """Decorator untuk JWT authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Simple JWT check - bisa dikembangkan lebih lanjut
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Missing authorization token'}), 401
        
        # Token validation logic here
        # For now, just check if token exists
        
        return f(*args, **kwargs)
    
    return decorated_function


def admin_required(f):
    """Decorator untuk admin authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is admin
        # Implementation depends on your authentication system
        
        return f(*args, **kwargs)
    
    return decorated_function
