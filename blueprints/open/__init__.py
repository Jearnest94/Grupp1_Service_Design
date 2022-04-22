from flask import Blueprint
from sqlalchemy import null

from models import User, Review
from flask import Flask, request, jsonify, make_response
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

bp_open = Blueprint('bp_open', __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, '123secret', algorithms=['HS256'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@bp_open.get('/user')
@token_required
def get_all_users(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function! check ur prividividididigeenena '})

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
@token_required
def get_one_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function! check ur privilegisifazj'})

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
@token_required
def create_user(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function! check ur privilegisifazj'})

    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    from app import db
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'New user created!'})


@bp_open.put('/user/<public_id>')
@token_required
def promote_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function! check ur privilegisifazj'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    user.admin = True
    from app import db
    db.session.commit()

    return jsonify({'message': 'The user has been promoted!'})


@bp_open.delete('/user/<public_id>')
@token_required
def delete_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function! check ur privilegisifazj'})

    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'No user found!'})

    from app import db
    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'The user has been deleted!'})


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
            {'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            '123secret')
        return jsonify({'token': token})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


@bp_open.get('/review')
@token_required
def get_all_reviews(current_user):
    reviews = Review.query.filter_by(user_id=current_user.id).all()

    output = []

    for review in reviews:
        review_data = {}
        review_data['id'] = review.id
        review_data['text'] = review.text
        review_data['rating'] = review.rating
        review_data['movie_id'] = review.movie_id
        output.append(review_data)

    return jsonify({'reviews': output})


@bp_open.get('/review/<review_id>')
@token_required
def get_one_review(current_user, review_id):
    review = Review.query.filter_by(id=review_id, user_id=current_user.id).first()

    if not review:
        return jsonify({'message': 'No review found'})

    review_data = {}
    review_data['id'] = review.id
    review_data['text'] = review.text
    review_data['rating'] = review.rating
    review_data['movie_id'] = review.movie_id

    return jsonify(review_data)


@bp_open.post('/review')
@token_required
def create_review(current_user):
    data = request.get_json()
    new_review = Review(text=data['text'], rating=data['rating'], movie_id=data['movie_id'], user_id=current_user.id)
    from app import db
    db.session.add(new_review)
    db.session.commit()

    return jsonify({'message': 'Review added!'})


@bp_open.put('/review/<review_id>')
@token_required
def set_rating(current_user, review_id):
    data = request.get_json()
    review = Review.query.filter_by(id=review_id, user_id=current_user.id).first()

    if not review:
        return jsonify({'message': 'No review found'})

    review.rating = data['rating']
    from app import db
    db.session.commit()

    return jsonify({'message': 'Rating adjusted.'})


@bp_open.delete('/review/<review_id>')
@token_required
def delete_review(current_user, review_id):
    review = Review.query.filter_by(id=review_id, user_id=current_user.id).first()

    if not review:
        return jsonify({'message': 'What no!? What do we delete+???'})

    from app import db
    db.session.delete(review)
    db.session.commit()

    return jsonify({'message': 'Review eradicated'})

