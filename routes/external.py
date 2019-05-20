import jwt
from datetime import datetime
from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash

from config import *
from functions import *

# Import all models and tables
from model import *


@app.route('{}/weather/<lat>/<lng>'.format(base_url), methods=['GET'])
@token_required
def get_weather(current_user):
    ## Exernal request to an external api and parse it
    output = {}

    return jsonify({'success': True, 'weather': output})
    


@app.route('{}/news/<lat>/<lng>'.format(base_url), methods=['GET'])
@token_required
def get_news(current_user):
    pass