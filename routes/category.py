from flask import request, jsonify, make_response

from config import *
from functions import *

# Import all models and tables
from model import *

# GET ALL CATEGORIES
@app.route('{}/categories'.format(base_url), methods=['GET'])
@token_required
def get_all_categories(current_user):
    categories = Category.query.all()

    output = []
    for category in categories:
        output.append(serialize_category(category))

    return jsonify({'success': True, 'categories': output})
    

# GET A CATEGORY
@app.route('{}/category/<name>'.format(base_url), methods=['GET'])
@token_required
def get_category(current_user, name):
    category = Category.query.filter_by(name=name).first()

    if not category:
        return jsonify({'success': False, 'message': 'No category found'})

    return jsonify({ 'success': True, 'category': serialize_category(category) })


# CREATE A CATEGORY
@app.route('{}/category'.format(base_url), methods=['POST'])
@token_required
def create_category(current_user):
    data = request.get_json()

    new_category = Category()
    for key in Category.__dict__:
        if key in data.keys():
            setattr(new_category, key, data[key])
    
    db.session.add(new_category)

    try:
        db.session.commit()
    except:
        return jsonify({'success': False, 'message': 'Error on create'})

    return jsonify({'success': True, 'category': serialize_category(new_category)})


# UPDATE A CATEGORY
@app.route('{}/category/<name>'.format(base_url), methods=['PUT'])
@token_required
def update_category(current_user, name):
    category = Category.query.filter_by(name=name).first()

    if not category:
        return jsonify({'success': False, 'message': 'No category found'})

    data = request.get_json()
    for key in category.__dict__:
        if key in data.keys():
            setattr(category, key, data[key])

    try:
        db.session.commit()
    except:
        return jsonify({'success': False, 'message': 'Error on update'})

    return jsonify({'success': True, 'category': serialize_category(category) })


# DELETE A CATEGORY
@app.route('{}/category/<name>'.format(base_url), methods=['DELETE'])
@token_required
def delete_category(current_user, name):
    category = Category.query.filter_by(name=name).first()

    if not category:
        return jsonify({'success': False, 'message': 'No category found'})
    
    db.session.delete(category)
    db.session.commit()

    return jsonify({'success': True})
