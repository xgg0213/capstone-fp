from datetime import datetime, timedelta
import jwt
from flask import current_app
from functools import wraps
from flask import request, g

def generate_jwt(user):
    """
    Generate a JWT token for the user
    """
    payload = {
        'user_id': str(user.id),
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(days=1),  # 1 day expiration
        'iat': datetime.utcnow()
    }
    
    return jwt.encode(
        payload,
        current_app.config['JWT_SECRET_KEY'],
        algorithm='HS256'
    )

def verify_jwt(token):
    """
    Verify a JWT token and return the payload
    """
    try:
        payload = jwt.decode(
            token,
            current_app.config['JWT_SECRET_KEY'],
            algorithms=['HS256']
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def jwt_required(f):
    """
    Decorator to protect routes with JWT
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token or not token.startswith('Bearer '):
            return {'error': 'Missing or invalid token'}, 401
            
        token = token.split('Bearer ')[1]
        payload = verify_jwt(token)
        
        if not payload:
            return {'error': 'Invalid or expired token'}, 401
            
        # Add user info to request context
        g.user_id = payload['user_id']
        return f(*args, **kwargs)
        
    return decorated 