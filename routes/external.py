import jwt
import requests
from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash

from config import *
from functions import *

# Import all models and tables
from model import *

# GET WEATHER
@app.route('{}/weather'.format(base_url), methods=['GET'])
@token_required
def get_weather(current_user):
    # Exernal request to an external api and parse it
    url = "http://api.openweathermap.org/data/2.5/weather"

    params = dict(
        lat = request.args.get('lat'),
        lon = request.args.get('lng'),
        units = "metric",
        lang = request.args.get('lang') if request.args.get('lang') is not None else 'fr',
        appid = OPENWEATHER_API_KEY
    )
    response =  requests.get(url=url, params=params)
    data = response.json()

    return jsonify({'success': True, 'weather': parse_weather(data)})

# GET NEWS
@app.route('{}/news'.format(base_url), methods=['GET'])
@token_required
def get_news(current_user):
    # External request
    url = "http://eventregistry.org/api/v1/article/getArticles"

    params = dict(
        locationUri = "http://en.wikipedia.org/wiki/{}".format(current_user.city[0].upper() + current_user.city[1:]), # Upper the firs letter
        lang = 'eng' if request.args.get('lang') is not None and request.args.get('lang') == 'en' else 'fra',
        apiKey = NEWS_API_KEY
    )
    
    res = requests.get(url=url, params=params)
    data = res.json()

    return jsonify({'success': True, 'articles': parse_articles(data)})