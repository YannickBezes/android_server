import jwt
from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash

from config import *
from functions import *

# Import all models and tables
from model import *


# GET ALL SHOPS
@app.route('{}/shops'.format(base_url), methods=['GET'])
@token_required
def get_all_shop(current_user):
    shops = Shop.query.all()

    output = []
    for shop in shops:
        output.append(serialize_shop(shop, user=current_user))

    return jsonify({'success': True, 'shops': output})


# GET ALL SHOPS BY CATEGORY
@app.route('{}/shops/<category_name>'.format(base_url), methods=['GET'])
@token_required
def get_all_shops_category(current_user, category_name):
    shops = Shop.query.all()
    category = Category.query.filter_by(name=category_name).first()

    if not category:
        return jsonify({'success': False, 'message': 'No category found'})

    output = []
    for shop in shops:
        if shop.category.name == category.name:
            output.append(serialize_shop(shop, user=current_user))
    
    return jsonify({'success': True, 'shops': output})


# GET ALL SHOPS WITCH ARE FAVORITE
@app.route('{}/shops/favorite'.format(base_url), methods=['GET'])
@token_required
def get_all_shops_favorite(current_user):
    output = []
    for shop in current_user.favorite_shops:
        output.append(serialize_shop(shop, user=current_user))
    
    return jsonify({'success': True, 'shops': output})


# GET ALL SHOPS LOCATION
@app.route('{}/shops/location'.format(base_url), methods=['GET'])
@token_required
def get_all_shops_location(current_user):
    shops = Shop.query.all()


    output = []
    for shop in shops:
        output.append(serialize_shop(shop, user=current_user))
    
    # Sort by distance
    output = sort_by_distance(output, request.args.get('lat'), request.args.get('lng'))

    return jsonify({'success': True, 'shops': output})


# GET SHOPS INTEREST
@app.route('{}/shops/interest'.format(base_url), methods=['GET'])
@token_required
def get_al_shops_interest(current_user):
    shops = Shop.query.all()

    output = []
    for shop in shops:
        is_a_keyword = False
        if current_user.interest and len(current_user.interest) > 0 and shop.keywords and len(shop.keywords) > 0:
            for keyword in [k.lower() for k in shop.keywords.split(',')]:
                if keyword in [i.lower() for i in current_user.interest.split(',')]:
                    is_a_keyword = True
            if is_a_keyword:
                output.append(serialize_shop(shop, user=current_user))
        else:
            return jsonify({'success': False, 'message': 'No interests given'})

    return jsonify({'success': True, 'shops': output})


# GET A SHOP
@app.route('{}/shop/<name>'.format(base_url), methods=['GET'])
@token_required
def get_shop(current_user, name):
    shop = Shop.query.filter_by(name=name).first()

    if not shop:
        return jsonify({'success': False, 'message': 'No shop found'})

    return jsonify({'success': True, 'shop': serialize_shop(shop, user=current_user)})


# CREATE A SHOP
@app.route('{}/shop'.format(base_url), methods=['POST'])
@token_required
def create_shop(current_user):
    data = request.get_json()

    # Get the category
    category = Category.query.filter_by(name=data['category']).first()

    if not category:
        return jsonify({'success': False, 'message': 'No category found'})
    data['category'] = category # Replace category string by an instance of category

    # Add all properties
    new_shop = Shop()
    for key in Shop.__dict__:
        if key in data.keys():
            setattr(new_shop, key, data[key])

    db.session.add(new_shop)
    try:
        db.session.commit()
    except:
        return jsonify({'success': False, 'message': 'Error on create'})

    return jsonify({'success': True, 'shop': serialize_shop(new_shop)})


# UPDATE A SHOP
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
        return jsonify({'success': False, 'message': 'Error on update'})

    return jsonify({'success': True, 'shop': serialize_shop(shop) })


# DELETE A SHOP
@app.route('{}/shop/<name>'.format(base_url), methods=['DELETE'])
@token_required
def delete_shop(current_user, name):
    shop = Shop.query.filter_by(name=name).first()

    if not shop:
        return jsonify({'success': False, 'message': 'No shop found'})
    
    db.session.delete(shop)
    db.session.commit()

    return jsonify({'success': True})
