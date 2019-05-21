import jwt
from datetime import datetime
from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash

from config import *
from functions import *

# Import all models and tables
from model import *

# GET ALL NETWORKS
@app.route('{}/networks'.format(base_url), methods=['GET'])
def get_all_group():
    groups = Group.query.all()

    output = []
    for group in groups:
        output.append(serialize_network(group))

    return jsonify({'success': True, 'networks': output})
    
# GET NEWORKS OF A USER
@app.route('{}/network'.format(base_url), methods=['GET'])
@token_required
def get_all_group_user(current_user):
    groups = Group.query.all()

    output = []
    for group in groups:
        # Check if the user is suscribe to the group
        if current_user in group.subscribers:
            output.append(serialize_network(group))
        
    return jsonify({'success': True, 'networks': output})

# GET A NETWORK
@app.route('{}/network/<name>'.format(base_url), methods=['GET'])
@token_required
def get_group(current_user, name):
    group = Group.query.filter_by(name=name).first()

    if not group:
        return jsonify({'success': False, 'message': 'No group found'})

    if group.public == False and current_user not in group.subscribers:
        return jsonify({'success': False, 'message': 'You don\'t have the right to access to this group'})    

    return jsonify({'success': True, 'data': serialize_network(group)})

# GET ALL POSTS FROM A NETWORK
@app.route('{}/network/<name>/posts'.format(base_url), methods=['GET'])
@token_required
def get_posts(current_user, name):
    group = Group.query.filter_by(name=name).first()

    if not group:
        return jsonify({'success': False, 'message': 'No group found'})
    
    if group.public == False and current_user not in group.subscribers:
        return jsonify({'success': False, 'message': 'You don\'t have the right to acces to this group'})
    
    return jsonify({'success': True, 'data': serialize_network(group, only_message=True)})


# CREATE A GROUP
@app.route('{}/network'.format(base_url), methods=['POST'])
@token_required
def create_group(current_user):
    data = request.get_json()

    # Check if group already exist
    is_exist = Group.query.filter_by(name=data['name']).first() is not None
    if is_exist:
        return jsonify({'success': False, 'message': "Group already exist"})

    new_group = Group() # Create the new group
    for key in Group.__dict__:
        if key in data.keys():
            setattr(new_group, key, data[key])
    
    # Add current_user to the group
    new_group.subscribers.append(current_user)

    # Update database
    db.session.add(new_group)
    db.session.commit()
    return jsonify({'success': True, 'data': serialize_network(new_group)})

# ADD A POST TO A GROUP
@app.route('{}/network/<name>'.format(base_url), methods=['POST'])
@token_required
def post_message(current_user, name):
    data = request.get_json()

    # Check if group already exist
    group = Group.query.filter_by(name=name).first()
    if not Group:
        return jsonify({'success': False, 'message': 'No group found'})
    
    post = Post(date=datetime.now().strftime("%d/%m/%Y-%H:%M"), content=data['content'])
    post.user = current_user # Add current user to the post as the sender
    group.posts.append(post)

    db.session.commit()

    return jsonify({'success': True, 'data': {}})

# ADD A USER TO A GROUP
@app.route('{}/network/<name>/<username>'.format(base_url), methods=['PUT'])
@token_required
def add_user(current_user, name, username):
    group = Group.query.filter_by(name=name).first()
    if not group:
        return jsonify({'success': False, 'message': 'No network found'})

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'success': False, 'message': 'No user found'})
    
    if user not in group.subscribers:
        group.subscribers.append(user)

    db.session.commit()

    return jsonify({'success': True, 'data': serialize_network(group)})


# SUB REQUEST
@app.route('{}/network/<name>/request'.format(base_url), methods=['PUT'])
@token_required
def sub_request(current_user, name):
    group = Group.query.filter_by(name=name).first()

    if not group:
        return jsonify({'success': False, 'message': 'No network found'})

    if current_user not in group.sub_requests:
        group.sub_requests.append(current_user)
    db.session.commit()

    return jsonify({'success': True})


# ACCEPT A SUB REQUEST
@app.route('{}/network/<name>/accept/<username>'.format(base_url), methods=['PUT'])
@token_required
def accept_sub_request(current_user, name, username):
    group = Group.query.filter_by(name=name).first() # Get the first group/network

    if not group: # If the network doesn't exist -> ERROR
        return jsonify({'success': False, 'message': 'No network found'})

    # If the current user is not a subscriber of the group he can't accept the sub request
    if current_user not in group.subscribers:
        return jsonify({'success': False, 'message': 'You don\'t have the right'})
    
    user = User.query.filter_by(username=username).first() # Get the user wich we want to add

    if not user:
        return jsonify({'success': False, 'message': 'User does not exist'})

    if user not in group.sub_requests:
        return jsonify({'success': False, 'message': 'User does not have send a request to this network'})

    # Delete the user from sub request and add it in subscribers
    group.sub_requests.remove(user)
    group.subscribers.append(user)
    db.session.commit()

    return jsonify({'success': True})
    

# UPDATE A NETWORK
@app.route('{}/network/<name>'.format(base_url), methods=['PUT'])
@token_required
def update_group(current_user, name):
    group = Group.query.filter_by(name=name).first()
    if not group:
        return jsonify({'success': False, 'message': 'No group found'})
    
    print current_user
    if current_user not in group.subscribers:
        return jsonify({'success': False, 'message': 'You don\'t have the right to modify this group'})
    
    data = request.get_json()
    for key in group.__dict__:
        if key in data.keys():
            setattr(group, key, data[key])
    
    try:
        db.session.commit()
    except:
        return jsonify({'success': False, 'message': 'Name already use'})

    return jsonify({'success': True, 'data': serialize_network(group)})


# DELETE A NETWORK
@app.route('{}/network/<name>'.format(base_url), methods=['DELETE'])
@token_required
def delete_group(current_user, name):
    group = Group.query.filter_by(name=name).first()
    if not group:
        return jsonify({'success': False, 'message': 'No group found'})

    if current_user not in group.subscribers:
        return jsonify({'success': False, 'message': 'You don\'t have the right to delete this group'})
    
    db.session.delete(group)
    db.session.commit()

    return jsonify({'success': True, 'data': serialize_network(group)})
