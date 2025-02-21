# Use below code to generate a secure random string for the JWT_SECRET_KEY and SECRET_KEY
# Both keys are added to the .env file
import secrets

# Generate a secure random string
jwt_secret = secrets.token_hex(32)
print(f"JWT_SECRET_KEY={jwt_secret}")