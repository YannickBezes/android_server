import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, jsonify, make_response

from config import *

# Import all models and tables
from model import *

@app.route('{}/login'.format(base_url))
def login():
    auth = request.get_json()

    auth['password'] = auth['password'].decode('base64') # Decode password

    if not auth or not auth['username'] or not auth['password']:
        return make_response('Could not verify your auth', 401, {'WWW-Authenticate': 'Basic realm="Login required:"'})
    
    user = User.query.filter_by(username=auth['username']).first()

    if not user:
        return make_response('Could not verify your auth', 401, {'WWW-Authenticate': 'Basic realm="Login required:"'})
    
    if check_password_hash(user.password, auth['password']):
        token = jwt.encode({'username': user.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)}, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})
        
    return make_response('Could not verify your auth', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
