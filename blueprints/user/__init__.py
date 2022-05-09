"""
CRUD for endpoint user
"""
import uuid

from flask import Blueprint
from werkzeug.security import generate_password_hash

from controllers.user_control import token_required
from models import User
from flask import request, jsonify

bp_user = Blueprint('bp_user', __name__)


@bp_user.get('/user')
@token_required
def get_all_users(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function! Check your privilegies.'}), 403

    users = User.query.all()

    output = []
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)
    return jsonify({'users': output}), 200


@bp_user.get('/user/<public_id>')
@token_required
def get_one_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function! Check your privilegies.'}), 403

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found!'}), 204

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin

    return jsonify({'user': user_data}), 200


@bp_user.post('/user')
@token_required
def create_user(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function! Check your privilegies.'}), 403

    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    username = data['name']
    from app import db
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': f'User with username {username} created!'}), 200


@bp_user.put('/user/<public_id>')
@token_required
def promote_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function! Check your privilegies.'}), 403

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found!'}), 404

    user.admin = True
    from app import db
    db.session.commit()

    return jsonify({'message': f'The user has been promoted to admin.'}), 200


@bp_user.delete('/user/<public_id>')
@token_required
def delete_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function! Check your privilegies.'}), 403

    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'No user found!'}), 204

    from app import db
    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': f'User has been deleted!'}), 200
