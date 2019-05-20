import jwt
import requests
from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash

from config import *
from functions import *

# Import all models and tables
from model import *


@app.route('{}/weather'.format(base_url), methods=['GET'])
@token_required
def get_weather(current_user):
    ## Exernal request to an external api and parse it
    url = "http://api.openweathermap.org/data/2.5/weather"

    params = dict(
        lat=request.args.get('lat'),
        lon=request.args.get('lng'),
        units="metric",
        lang=request.args.get('lang'),
        appid=OPENWEATHER_API_KEY
    )
    response =  requests.get(url=url, params=params)
    data = response.json()

    output = parse_weather(data)

    return jsonify({'success': True, 'weather': output})
    


@app.route('{}/news/<lat>/<lng>'.format(base_url), methods=['GET'])
@token_required
def get_news(current_user):
    pass