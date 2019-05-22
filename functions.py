import jwt
import datetime
import math
import decimal
from flask import request, jsonify
from functools import wraps
from config import app
from model import *

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
    for key in User.__dict__:
        if key[0] != '_' and key not in ['password', 'id', 'subscription_requests']:
            if key == 'subscriptions':
                user_data[key] = []
                for network in user.subscriptions:
                    user_data[key].append(network.name)
            else:
                user_data[key] = getattr(user, key)

    return user_data


def serialize_network(network, only_message=False, only_sub_request=False):
    """
    Method for serialize a network
    """
    network_data = {}
    if not only_sub_request:
        if not only_message:
            network_data['name'] = network.name
            network_data['public'] = network.public
            network_data['subscribers'] = []
            for user in network.subscribers:
                network_data['subscribers'].append(user.username)
            network_data['sub_requests'] = []
            for user in network.sub_requests:
                network_data['sub_requests'].append(user.username)

        # Parse messages
        network_data['posts'] = []
        for post in network.posts:
            network_data['posts'].append({"sender": post.user.username, "date": post.date, "content": post.content})
        
        network_data['posts'].reverse() # Reverse to add the last post in first
    else:
        # If we want only sub request create a list with all sub requests
        network_data = []
        for user in network.sub_requests:
            network_data.append(user.username)

    return network_data


def serialize_shop(shop):
    shop_data = {}

    for key in Shop.__dict__:
        if key[0] != '_' and key not in ['id', 'category_id']:
            shop_data[key] = getattr(shop, key)
    
    shop_data['category'] = serialize_category(shop.category, shop=False)

    return shop_data


def serialize_category(category, shop=True):
    category_data = {}

    for key in Category.__dict__:
        if key[0] != '_' and key not in ['id']:
            category_data[key] = getattr(category, key)

    if shop:
        category_data['shops'] = []
        for shop in category.shops:
            category_data['shops'].append(shop.name)    
    else:
        del category_data['shops']
    
    return category_data

def parse_weather(weather):
    output = {}

    for key in weather.keys():
        if key not in ['base', 'cod', 'coord', 'dt', 'id', 'rain', 'sys']:
            if key in 'weather':
                for sub_key in weather[key][0]:
                    output[sub_key] = weather[key][0][sub_key]
            else:
                if key in 'main':
                    for sub_key in weather[key]:
                        output[sub_key] = weather[key][sub_key]
                else:
                    if key in 'clouds':
                        output[key] = weather[key]['all']
                    else:
                        output[key] = weather[key]

    del output['icon'], output['id']
    return output


def parse_articles(articles):
    output = []

    # Select articles
    articles = articles['articles']['results']

    for article in articles:
        for key in ['dataType', 'eventUri', 'isDuplicate', 'lang', 'sentiment', 'sim', 'date', 'time', 'uri', 'wgt', 'authors']:
            del article[key] # Delete key that we don't want

        article['dateTime'] = datetime.datetime.strptime(article['dateTime'][:-1], '%Y-%m-%dT%H:%M:%S').strftime('%d/%m/%Y-%H:%M')
        article['source'] = article['source']['title'] # Just put the title as a source

        output.append(article)

    return output


def distance(lat_1, lng_1, lat_2, lng_2):
    D = decimal.Decimal

    dist = math.sqrt((D(lat_2) - D(lat_1))**2 + (D(lng_2) - D(lng_1))**2)
    return dist


def sort_by_distance(arr, lat, lng):
    for i in range(len(arr)):
        cursor = arr[i]
        pos = i
        
        while pos > 0 and distance(lat, lng, arr[pos - 1]['lat'], arr[pos - 1]['lng']) > distance(lat, lng, cursor['lat'], cursor['lng']):
            # Swap the number down the list
            arr[pos] = arr[pos - 1]
            pos -= 1
        # Break and do the final swap
        arr[pos] = cursor

    return arr