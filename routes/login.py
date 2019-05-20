import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, jsonify, make_response

from config import *

# Import all models and tables
from model import *

@app.route('{}/login'.format(base_url), methods=['POST'])
def login():
    auth = request.get_json()

    if not auth or not auth['username'] or not auth['password']:
        return jsonify({'success': False, 'message': "Login required"})
    
    user = User.query.filter_by(username=auth['username']).first()

    if not user:
        return jsonify({'success': False, 'message': "Login required"})
    
    if check_password_hash(user.password, auth['password']):
        token = jwt.encode({'username': user.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)}, app.config['SECRET_KEY'])
        return jsonify({'success': True, 'token': token.decode('UTF-8')})
        
    return jsonify({'success': False, 'message': "Login required"})
