import os

from flask import Blueprint

from models import User, Log
from flask import request, jsonify, make_response
from werkzeug.security import check_password_hash
import jwt
import datetime

bp_open = Blueprint('bp_open', __name__)


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
            {'id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=600)},
            os.getenv("APP_SECRET"))
        from app import db
        user.latesttoken = token
        db.session.commit()
        return jsonify({'token': token}), 200

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


@bp_open.before_request
def logger():
    token = request.headers.get('x-access-token')
    print(token)
    now = datetime.datetime.utcnow()
    from sqlalchemy.sql.functions import current_user
    new_log = Log(user=current_user.name, endpoint=request.endpoint, timestamp=now)
    from app import db
    db.session.add(new_log)
    db.session.commit()
    print(f'API accessed {request.endpoint} \t {now.strftime("%Y-%m-%d %H:%M:%S")}')



