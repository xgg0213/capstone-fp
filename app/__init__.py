import os
from flask import Flask, render_template, request, session, redirect
from flask_cors import CORS
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_login import LoginManager
from flask_socketio import SocketIO
from .commands import init_commands

# Create Flask app first
app = Flask(__name__, static_folder='../react-vite/dist', static_url_path='/')

# Import config after app creation
from .config import Config
app.config.from_object(Config)

# Import models after app creation
from .models import db, User

# Initialize core extensions
db.init_app(app)
migrate = Migrate(app, db)

# Setup login manager
login = LoginManager(app)
login.login_view = 'auth.unauthorized'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# Import blueprints after models and extensions
from .api.user_routes import user_routes
from .api.auth_routes import auth_routes
from .api.transaction_routes import transaction_routes
from .api.stock_routes import stock_routes
from .api.test_routes import test_routes

# Import seeds after models
from .seeds import seed_commands

# Register blueprints
app.register_blueprint(user_routes, url_prefix='/api/users')
app.register_blueprint(auth_routes, url_prefix='/api/auth')
app.register_blueprint(transaction_routes, url_prefix='/api/transactions')
app.register_blueprint(stock_routes, url_prefix='/api/stocks')
app.register_blueprint(test_routes, url_prefix='/api/test')

# Initialize CLI commands
init_commands(app)

# Security
CORS(app)

# Import and initialize services last
from .services.websocket_service import socketio
from .services.market_data_service import market_data_service

socketio.init_app(app, 
    cors_allowed_origins="*",
    async_mode='gevent'
)

@app.before_first_request
def start_market_data():
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(market_data_service.connect_to_market_feed())
    loop.run_forever()

# Routes
@app.before_request
def https_redirect():
    if os.environ.get('FLASK_ENV') == 'production':
        if request.headers.get('X-Forwarded-Proto') == 'http':
            url = request.url.replace('http://', 'https://', 1)
            code = 301
            return redirect(url, code=code)

@app.after_request
def inject_csrf_token(response):
    response.set_cookie(
        'csrf_token',
        generate_csrf(),
        secure=True if os.environ.get('FLASK_ENV') == 'production' else False,
        samesite='Strict' if os.environ.get('FLASK_ENV') == 'production' else None,
        httponly=True)
    return response

@app.route("/api/docs")
def api_help():
    """Returns all API routes and their doc strings"""
    acceptable_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    route_list = { rule.rule: [[ method for method in rule.methods if method in acceptable_methods ],
                    app.view_functions[rule.endpoint].__doc__ ]
                    for rule in app.url_map.iter_rules() if rule.endpoint != 'static' }
    return route_list

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def react_root(path):
    if path == 'favicon.ico':
        return app.send_from_directory('public', 'favicon.ico')
    return app.send_static_file('index.html')

@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')
