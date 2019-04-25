import jwt
from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash

from config import *
from functions import *

# Import all models and tables
from model import *


@app.route('{}/shop'.format(base_url), methods=['GET'])
@token_required
def get_all_shop(current_user):
    shops = Shop.query.all()

    output = []
    for shop in shops:
        output.append(serialize_shop(shop))

    return jsonify({'success': True, 'shops': output})
    

@app.route('{}/shop/<name>'.format(base_url), methods=['GET'])
@token_required
def get_shop(current_user, name):
    shop = Shop.query.filter_by(name=name).first()

    if not shop:
        return jsonify({'success': False, 'message': 'No shop found'})

    return jsonify({ 'success': True, 'data': serialize_shop(shop) })


@app.route('{}/shop'.format(base_url), methods=['POST'])
def create_shop():
    data = request.get_json()

    new_shop = Shop()
    for key in Shop.__dict__:
        if key in data.keys():
            setattr(new_shop, key, data[key])
    
    db.session.add(new_shop)

    try:
        db.session.commit()
    except:
        return jsonify({'success': False, 'message': 'Name already use'})

    return jsonify({'success': True, 'data': serialize_shop(new_shop)})


@app.route('{}/shop/<name>'.format(base_url), methods=['PUT'])
@token_required
def update_shop(current_user, name):
    shop = Shop.query.filter_by(name=name).first()

    if not shop:
        return jsonify({'success': False, 'message': 'No shop found'})

    data = request.get_json()
    for key in shop.__dict__:
        if key in data.keys():
            setattr(shop, key, data[key])

    try:
        db.session.commit()
    except:
        return jsonify({'success': False, 'message': 'Username already use'})

    return jsonify({'success': True, 'data': serialize_shop(shop) })


@app.route('{}/shop/<name>'.format(base_url), methods=['DELETE'])
@token_required
def delete_shop(current_user, username):
    shop = Shop.query.filter_by(name=name).first()

    if not shop:
        return jsonify({'success': False, 'message': 'No shop found'})
    
    db.session.delete(shop)
    db.session.commit()

    return jsonify({'success': True, 'data': serialize_shop(shop)})
