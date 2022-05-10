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
        return jsonify({'message': 'Cannot perform that function! Check your privilegies.'}), 403

    users = User.query.all()

    output = []
    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        user_data['links'] = {
            'This user:': f'/api/v1.0/user/{user.id}',
            'Reviews by this user': f'/api/v1.0/review/user/{user.id}'
        }
        output.append(user_data)
    return jsonify({'users': output}), 200


@bp_user.get('/user/<id>')
@token_required
def get_one_user(current_user, id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function! Check your privilegies.'}), 403

    user = User.query.filter_by(id=id).first()

    if not user:
        return jsonify({'message': 'No user found!'}), 204

    user_data = {}
    user_data['id'] = user.id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin
    user_data['links'] = {
        'All users:': f'/api/v1.0/user',
        'Reviews by this user': f'/api/v1.0/review/user/{user.id}',
        'Promote user(PUT)': f'/api/v1.0/user/{user.id}'
    }

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
    last_added_user = User.query.order_by(User.id.desc()).first()
    return jsonify({'message': f'User with username {username} created!', 'All users:': f'/api/v1.0/user', 'New user': f'/api/v1.0/user/{last_added_user.id}',
                    'Promote new user': f'/api/v1.0/user/{last_added_user.id}'}), 200


@bp_user.put('/user/<id>')
@token_required
def promote_user(current_user, id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function! Check your privilegies.'}), 403

    user = User.query.filter_by(id=id).first()

    if not user:
        return jsonify({'message': 'No user found!'}), 404

    user.admin = True
    from app import db
    db.session.commit()

    return jsonify({'message': f'The user has been promoted to admin.', 'All users:': f'/api/v1.0/user', 'Promoted user': f'/api/v1.0/user/{user.id}'}), 200


@bp_user.delete('/user/<id>')
@token_required
def delete_user(current_user, id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function! Check your privilegies.'}), 403

    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({'message': 'No user found!'}), 204

    from app import db
    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': f'User has been deleted!', 'All users:': f'/api/v1.0/user'}), 200


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
