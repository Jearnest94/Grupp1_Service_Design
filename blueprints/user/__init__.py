"""
CRUD for endpoint user
"""
import datetime
import uuid

from flask import Blueprint
from werkzeug.security import generate_password_hash

from controllers.user_control import token_required
from models import User, Log
from flask import request, jsonify

bp_user = Blueprint('bp_user', __name__)


@bp_user.get('/user')
@token_required
def get_all_users(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function! Check your privileges.'}), 403

    users = User.query.all()

    output = []
    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)
    return jsonify({'users': output}), 200


@bp_user.get('/user/<id>')
@token_required
def get_one_user(current_user, id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function! Check your privileges.'}), 403

    user = User.query.filter_by(id=id).first()

    if not user:
        return jsonify({'message': 'No user found!'}), 404

    user_data = {}
    user_data['id'] = user.id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin

    return jsonify({'user': user_data}), 200


@bp_user.post('/user')
@token_required
def create_user(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function! Check your privileges.'}), 403

    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    username = data['name']
    from app import db
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': f'User with username {username} created!'}), 201


@bp_user.put('/user/<id>')
@token_required
def promote_user(current_user, id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function! Check your privileges.'}), 403

    user = User.query.filter_by(id=id).first()

    if not user:
        return jsonify({'message': 'No user found!'}), 404

    user.admin = True
    from app import db
    db.session.commit()

    return jsonify({'message': f'The user has been promoted to admin.'}), 200


@bp_user.delete('/user/<id>')
@token_required
def delete_user(current_user, id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function! Check your privilegies.'}), 403

    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({'message': 'No user found!'}), 404

    from app import db
    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': f'User has been deleted!'}), 200


@bp_user.before_request
def logger():
    token = request.headers.get('x-access-token')
    user = User.query.filter_by(latesttoken=token).first()
    now = datetime.datetime.utcnow()
    new_log = Log(user=user.name, endpoint=request.endpoint, timestamp=now)
    from app import db
    db.session.add(new_log)
    db.session.commit()
    print(f'API Accessed - User: {user.name} - Endpoint: {request.endpoint} \t {now.strftime("%Y-%m-%d %H:%M:%S")}')
