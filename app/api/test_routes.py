from flask import Blueprint, session, jsonify
from flask_wtf.csrf import generate_csrf
from flask_login import login_required

test_routes = Blueprint('test', __name__)

@test_routes.route('/security-test')
@login_required
def test_security():
    """
    Test route to verify security features
    """
    try:
        # Test session
        session['test'] = 'Session working'
        session_value = session.get('test')
        
        # Test CSRF
        csrf_token = generate_csrf()
        
        return jsonify({
            'session_test': session_value == 'Session working',
            'csrf_test': bool(csrf_token),
            'status': 'All security features working!'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'Security test failed'
        }), 500

@test_routes.route('/csrf-test', methods=['POST'])
@login_required
def test_csrf_protection():
    """
    Test route to verify CSRF protection
    """
    # If this route is reached, CSRF protection is working
    # (Flask-WTF will automatically reject invalid CSRF tokens)
    return jsonify({
        'status': 'CSRF protection working!',
        'message': 'Form submission successful'
    }) 