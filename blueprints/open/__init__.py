from flask import Blueprint
from models import User
from flask import Flask, request, jsonify
import uuid
from werkzeug.security import generate_password_hash, check_password_hash


bp_open = Blueprint('bp_open', __name__)


@bp_open.get('/user')
def get_all_users():
    users = User.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)
    return jsonify({'users': output})


@bp_open.get('/user/<public_id>')
def get_one_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin

    return jsonify({'user': user_data})


@bp_open.post('/user')
def create_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    from app import db
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'New user created!'})


@bp_open.put('/user/<public_id>')
def promote_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    user.admin = True
    from app import db
    db.session.commit()

    return jsonify({'message': 'The user has been promoted!'})


@bp_open.delete('/user/<public_id>')
def delete_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    from app import db
    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'The user has been deleted!'})
