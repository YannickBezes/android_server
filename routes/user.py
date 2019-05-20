import jwt
import datetime
from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash

from config import *
from functions import *

# Import all models and tables
from model import *


@app.route('{}/user'.format(base_url), methods=['GET'])
# @token_required
def get_all_user():
    if request.method == "POST":
        print request.get_json()
    users = User.query.all()

    output = []
    for user in users:
        output.append(serialize_user(user))

    return jsonify({'success': True, 'users': output})
    

@app.route('{}/user/<username>'.format(base_url), methods=['GET'])
@token_required
def get_user(current_user, username):
    if current_user.username != username:
        return jsonify({ 'success': False, 'message': 'You can\'t access to this user' })

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'success': False, 'message': 'No user found'})

    return jsonify({ 'success': True, 'data': serialize_user(user) })


@app.route('{}/user'.format(base_url), methods=['POST'])
def create_user():
    data = request.get_json()

    new_user = User()
    for key in User.__dict__:
        if key in data.keys():
            if key == 'password':
                setattr(new_user, key, generate_password_hash(data['password'], method='sha512'))
            else:
                setattr(new_user, key, data[key])
    
    db.session.add(new_user)

    try:
        db.session.commit()
    except:
        return jsonify({'success': False, 'message': 'Username already use'})

    token = jwt.encode({'username': new_user.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)}, app.config['SECRET_KEY'])

    return jsonify({'success': True, 'token': token})


@app.route('{}/user/<username>'.format(base_url), methods=['PUT'])
@token_required
def update_user(current_user, username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'success': False, 'message': 'No user found'})

    data = request.get_json()
    for key in user.__dict__:
        if key in data.keys():
            if key == 'password':
                setattr(user, key, generate_password_hash(data['password'], method='sha512'))
            else:
                setattr(user, key, data[key])

    try:
        db.session.commit()
    except:
        return jsonify({'success': False, 'message': 'Username already use'})

    return jsonify({'success': True, 'data': serialize_user(user) })


@app.route('{}/user/<username>'.format(base_url), methods=['DELETE'])
@token_required
def delete_user(current_user, username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'success': False, 'message': 'No user found'})
    
    db.session.delete(user)
    db.session.commit()

    return jsonify({'success': True, 'data': serialize_user(user)})
