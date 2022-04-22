from flask import Blueprint
from app import db
from models import User
from flask import Flask, request, jsonify
import uuid
from werkzeug.security import generate_password_hash, check_password_hash


bp_open = Blueprint('bp_open', __name__)


@bp_open.get('/user')
def get_all_users():
    return ''


@bp_open.get('/user/<user_id>')
def get_one_user():
    return ''


@bp_open.post('/user')
def create_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    from app import db
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'New user created!'})


@bp_open.put('/user/<user_id>')
def promote_user():
    return ''


@bp_open.delete('/user/<user_id>')
def delete_user():
    return ''
