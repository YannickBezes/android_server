import jwt
from flask import request, jsonify
from functools import wraps
from config import app
from model.user import User

# Method for token check
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return jsonify({'success': False, 'message': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(username=data['username']).first()
            if current_user is None:
                return jsonify({'success': False, 'message': 'Token is invalid'}), 401    
        except:
            return jsonify({'success': False, 'message': 'Token is invalid'}), 401
        
        return f(current_user, *args, **kwargs)

    return decorated


def serialize_user(user):
    """
    Method for serialize an user
    """
    user_data = {}
    for key in user.__dict__:
        if key not in ['password', '_sa_instance_state', 'id']:
            user_data[key] = getattr(user, key)

    return user_data


def serialize_network(network, only_message=False):
    """
    Method for serialize a network
    """
    network_data = {}

    if not only_message:
        network_data['name'] = network.name
        network_data['public'] = network.public
        network_data['subscribers'] = []
        for user in network.subscribers:
            network_data['subscribers'].append(user.username)

    # Parse messages
    network_data['posts'] = []
    for post in network.posts:
        network_data['posts'].append({"sender": post.user.username, "date": post.date, "content": post.content})

    return network_data


def serialize_shop(shop):
    pass