from flask import Blueprint
from sqlalchemy import null

from controllers.user_control import token_required
from models import User, Review, Log, Movie
from flask import Flask, request, jsonify, make_response
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

bp_open = Blueprint('bp_open', __name__)


@bp_open.before_request
def logger():
    now = datetime.datetime.utcnow()
    from sqlalchemy.sql.functions import current_user
    new_log = Log(user=current_user.name, endpoint=request.endpoint, timestamp=now)
    from app import db
    db.session.add(new_log)
    db.session.commit()
    print(f'API accessed {request.endpoint} \t {now.strftime("%Y-%m-%d %H:%M:%S")}')


@bp_open.get('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.query.filter_by(name=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=600)},
            '123secret')
        from app import db
        user.latesttoken = token
        db.session.commit()
        return jsonify({'token': token})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})



