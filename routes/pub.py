from flask import request, jsonify, make_response

from config import *
from functions import *

# Import all models and tables
from model import *


# GET ALL PUB
@app.route('{}/pubs'.format(base_url), methods=['GET'])
@token_required
def get_all_pubs(current_user):
    pubs = Pub.query.all()

    output = []
    for pub in pubs:
        if current_user.interest and len(current_user.interest) > 0 and pub.keywords and len(pub.keywords) > 0:
            is_a_keyword = False
            for keyword in [k.lower() for k in pub.keywords.split(',')]:
                if keyword in [i.lower() for i in current_user.interest.split(',')]:
                    is_a_keyword = True
            if is_a_keyword:
                output.append(serialize_pub(pub))
        else:
            output.append(serialize_pub(pub))

    return jsonify({'success': True, 'pubs': output})


# CREATE A PUB
@app.route('{}/pub'.format(base_url), methods=['POST'])
@token_required
def create_pub(current_user):
    data = request.get_json()

    new_pub = Pub()
    for key in Pub.__dict__:
        if key in data.keys():
            setattr(new_pub, key, data[key])
    
    db.session.add(new_pub)

    try:
        db.session.commit()
    except:
        return jsonify({'success': False, 'message': 'Error on create'})

    return jsonify({'success': True, 'pub': serialize_pub(new_pub)})


# UPDATE A PUB
@app.route('{}/pub/<name>'.format(base_url), methods=['PUT'])
@token_required
def update_pub(current_user, name):
    pub = Pub.query.filter_by(name=name).first()

    if not pub:
        return jsonify({'success': False, 'message': 'No pub found'})

    data = request.get_json()
    for key in pub.__dict__:
        if key in data.keys():
            setattr(pub, key, data[key])

    try:
        db.session.commit()
    except:
        return jsonify({'success': False, 'message': 'Error on update'})

    return jsonify({'success': True, 'pub': serialize_pub(pub) })


# DELETE A PUB
@app.route('{}/pub/<name>'.format(base_url), methods=['DELETE'])
@token_required
def delete_pub(current_user, name):
    pub = Pub.query.filter_by(name=name).first()

    if not pub:
        return jsonify({'success': False, 'message': 'No pub found'})
    
    db.session.delete(pub)
    db.session.commit()

    return jsonify({'success': True})
