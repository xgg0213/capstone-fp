from flask import Blueprint, request, jsonify
from app.models import User, db
from app.forms import LoginForm
from app.forms import SignUpForm
from flask_login import current_user, login_user, logout_user, login_required
from flask_wtf.csrf import generate_csrf

auth_routes = Blueprint('auth', __name__)

def validation_errors_to_error_messages(validation_errors):
    """
    Simple function that turns the WTForms validation errors into a simple list
    """
    errorMessages = []
    for field in validation_errors:
        for error in validation_errors[field]:
            errorMessages.append(f'{field} : {error}')
    return errorMessages

@auth_routes.route('/')
def authenticate():
    """
    Authenticates a user.
    """
    if current_user.is_authenticated:
        return current_user.to_dict()
    return {'errors': {'message': 'Unauthorized check for home page'}}, 401

@auth_routes.route('/login', methods=['POST'])
def login():
    """
    Logs a user in
    """
    data = request.get_json()
    
    if not data:
        return {'errors': ['Invalid request data']}, 400
        
    user = User.query.filter(User.email == data.get('email')).first()
    
    if not user:
        return {'errors': ['Email provided not found.']}, 401
        
    if not user.check_password(data.get('password')):
        return {'errors': ['Password was incorrect.']}, 401
        
    login_user(user)
    return user.to_dict()

@auth_routes.route('/logout')
def logout():
    """
    Logs a user out
    """
    logout_user()
    return {'message': 'User logged out'}

@auth_routes.route('/signup', methods=['POST'])
def sign_up():
    """
    Creates a new user and logs them in
    """
    # try:
    print("Received signup request data:", request.get_json())  # Debug print
    
    form = SignUpForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    
    if not form.validate_on_submit():
        print("Form validation errors:", form.errors)  # Debug print
        print("check firstName: ", form.data)
        return form.errors, 401
    
    user = User(
        username=form.data['username'],
        email=form.data['email'],
        password=form.data['password'],
        first_name=form.data['first_name'],
        last_name=form.data['last_name']
    )
    
    db.session.add(user)
    db.session.commit()
    login_user(user)
    
    return user.to_dict()
        
    # except Exception as e:
    #     print("Signup error:", str(e))  # Debug print
    #     db.session.rollback()
    #     return {'errors': {'general': str(e)}}, 500

@auth_routes.route('/unauthorized')
def unauthorized():
    """
    Returns unauthorized JSON when flask-login authentication fails
    """
    return {'errors': {'message': 'Unauthorized'}}, 401

@auth_routes.route('/csrf/restore')
def get_csrf_token():
    """
    Get CSRF token
    """
    response = jsonify({"csrf_token": generate_csrf()})
    response.headers.set("XSRF-TOKEN", generate_csrf())
    return response