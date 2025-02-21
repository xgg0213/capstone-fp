# Handles how the app runs
# Kept outside of app/__init__.py to avoid circular imports and deployment flexibility

from app import app, socketio

if __name__ == '__main__':
    socketio.run(app, debug=True) 