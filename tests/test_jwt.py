from flask import Flask
import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

def test_jwt():
    # Load environment variables
    load_dotenv()
    
    jwt_secret = os.getenv('JWT_SECRET_KEY')
    
    if not jwt_secret:
        print("❌ Error: JWT_SECRET_KEY not found in .env file")
        return False
        
    try:
        # Create a test payload
        payload = {
            'user_id': '123',
            'email': 'test@example.com',
            'exp': datetime.utcnow() + timedelta(days=1)
        }
        
        # Generate token
        token = jwt.encode(payload, jwt_secret, algorithm='HS256')
        print("✅ JWT token generated successfully!")
        print(f"Token: {token[:20]}...")
        
        # Verify token
        try:
            decoded = jwt.decode(token, jwt_secret, algorithms=['HS256'])
            print("✅ JWT token verified successfully!")
            print(f"Decoded payload: {decoded}")
        except jwt.ExpiredSignatureError:
            print("❌ Token has expired")
            return False
        except jwt.InvalidTokenError as e:
            print(f"❌ Invalid token: {str(e)}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing JWT: {str(e)}")
        return False

if __name__ == "__main__":
    test_jwt() 