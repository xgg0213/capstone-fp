from flask import Blueprint, request, jsonify, make_response
from app.models import User, db
from app.forms import LoginForm, SignUpForm
from flask_login import current_user, login_user, logout_user, login_required
from app.utils.auth import get_auth_token, generate_jwt, verify_jwt
from flask_wtf.csrf import generate_csrf

auth_routes = Blueprint('auth', __name__)


@auth_routes.route('/')
def authenticate():
    """
    Authenticates a user.
    """
    if current_user.is_authenticated:
        return current_user.to_dict()
    return {'errors': {'message': 'Unauthorized'}}, 401


@auth_routes.route('/csrf/restore')
def restore_csrf():
    """
    Generates and returns a new CSRF token
    """
    response = make_response({'csrf_token': generate_csrf()})
    response.set_cookie('csrf_token', generate_csrf())
    return response


@auth_routes.route('/register', methods=['POST'])
def register():
    """
    Creates a new user and returns their info with auth token
    """
    form = SignUpForm()
    # Get the csrf_token from the request cookie and put it into the
    # form manually to validate_on_submit can be used
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        user = User(
            email=form.data['email'],
            password=form.data['password'],
            first_name=form.data['first_name'],
            last_name=form.data['last_name']
        )
        db.session.add(user)
        db.session.commit()
        
        token = get_auth_token(user)
        response = make_response({
            'user_id': str(user.id),
            'token': token
        })
        response.status_code = 201
        return response
    return {'error': {'message': 'Invalid registration data', 'details': form.errors}}, 400


@auth_routes.route('/login', methods=['POST'])
def login():
    """
    Logs a user in with both JWT and CSRF protection
    """
    form = LoginForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    
    if form.validate_on_submit():
        user = User.query.filter(User.email == form.data['email']).first()
        if user and user.check_password(form.data['password']):
            # Generate JWT for API authentication
            jwt_token = generate_jwt(user)
            
            # Generate CSRF token for form submissions
            csrf_token = generate_csrf()
            
            response = make_response({
                'token': jwt_token,
                'user': user.to_dict()
            })
            
            # Set CSRF token in cookie
            response.set_cookie('csrf_token', csrf_token)
            
            return response
            
    return {'error': 'Invalid credentials'}, 401


@auth_routes.route('/logout', methods=['POST'])
@login_required
def logout():
    """
    Logs a user out
    """
    logout_user()
    return {'message': 'Successfully logged out'}, 200


@auth_routes.route('/unauthorized')
def unauthorized():
    """
    Returns unauthorized JSON when flask-login authentication fails
    """
    return {'errors': {'message': 'Unauthorized'}}, 401


@auth_routes.route('/protected', methods=['POST'])
@jwt_required  # Checks JWT
def protected_route():
    """
    Example of route protected by both JWT and CSRF
    """
    # JWT already verified by decorator
    # CSRF verified by Flask-WTF
    form = SomeForm()
    if form.validate_on_submit():  # This checks CSRF
        # Process the request
        return {'success': True}
    return {'error': 'Invalid request'}, 400