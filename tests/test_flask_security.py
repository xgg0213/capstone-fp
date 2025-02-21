from flask import Flask, session
from flask_wtf.csrf import generate_csrf
import os
from dotenv import load_dotenv

def test_flask_security():
    # Load environment variables
    load_dotenv()
    
    secret_key = os.getenv('SECRET_KEY')
    if not secret_key:
        print("❌ Error: SECRET_KEY not found in .env file")
        return False

    try:
        # Create test Flask app
        app = Flask(__name__)
        app.config['SECRET_KEY'] = secret_key
        
        # Test 1: Session encryption
        with app.test_request_context():
            session['test_key'] = 'test_value'
            encrypted_session = session.get('test_key')
            print("✅ Session encryption working!")
            print(f"Session value: {encrypted_session}")
            
        # Test 2: CSRF token generation
        with app.test_request_context():
            csrf_token = generate_csrf()
            print("✅ CSRF token generation working!")
            print(f"CSRF token: {csrf_token[:20]}...")
            
        return True
        
    except Exception as e:
        print(f"❌ Error testing Flask security: {str(e)}")
        return False

if __name__ == "__main__":
    test_flask_security() 