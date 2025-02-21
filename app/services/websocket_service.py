from flask_socketio import SocketIO, emit, join_room, leave_room
from app.models import User, Portfolio
from flask_login import current_user
import json

socketio = SocketIO()

# Track connected clients and their subscriptions
clients = {}

@socketio.on('connect')
def handle_connect():
    """Handle new WebSocket connections"""
    if not current_user.is_authenticated:
        return False
    
    clients[current_user.id] = {
        'session_id': request.sid,
        'subscriptions': set()  # Track subscribed symbols
    }

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnections"""
    if current_user.id in clients:
        del clients[current_user.id]

@socketio.on('subscribe')
def handle_subscribe(data):
    """
    Handle subscription to stock price updates
    data = {'symbols': ['AAPL', 'GOOGL']}
    """
    if not current_user.is_authenticated:
        return
    
    symbols = set(symbol.upper() for symbol in data.get('symbols', []))
    clients[current_user.id]['subscriptions'].update(symbols)
    
    # Join rooms for each symbol
    for symbol in symbols:
        join_room(f"price_updates_{symbol}")

@socketio.on('unsubscribe')
def handle_unsubscribe(data):
    """
    Handle unsubscription from stock price updates
    """
    if not current_user.is_authenticated:
        return
        
    symbols = set(symbol.upper() for symbol in data.get('symbols', []))
    clients[current_user.id]['subscriptions'].difference_update(symbols)
    
    # Leave rooms for each symbol
    for symbol in symbols:
        leave_room(f"price_updates_{symbol}")

def broadcast_price_update(symbol, price_data):
    """
    Broadcast price updates to subscribed clients
    """
    room = f"price_updates_{symbol}"
    emit('price_update', {
        'symbol': symbol,
        'price': price_data['price'],
        'change': price_data['change'],
        'change_percent': price_data['change_percent'],
        'timestamp': price_data['timestamp']
    }, room=room) 