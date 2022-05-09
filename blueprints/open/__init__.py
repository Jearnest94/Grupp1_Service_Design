from flask import Blueprint
from sqlalchemy import null


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
        return jsonify({'message': 'Cannot perform that function! Check your privilegies.'})

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
        return jsonify({'message': 'Cannot perform that function! Check your privilegies.'})

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
        return jsonify({'message': 'Cannot perform that function! Check your privilegies.'})

    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    username = data['name']
    from app import db
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': f'User with username {username} created!'})


@bp_open.put('/user/<public_id>')
@token_required
def promote_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function! Check your privilegies.'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    user.admin = True
    from app import db
    db.session.commit()

    return jsonify({'message': f'The user has been promoted to admin.'})


@bp_open.delete('/user/<public_id>')
@token_required
def delete_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function! Check your privilegies.'})

    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'No user found!'})

    from app import db
    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': f'User has been deleted!'})


@bp_open.get('/review')
@token_required
def get_all_reviews(current_user):
    reviews = Review.query.all()

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
    review = Review.query.filter_by(id=review_id).first()

    if not review:
        return jsonify({'message': 'No review found'})

    review_data = {}
    review_data['id'] = review.id
    review_data['text'] = review.text
    review_data['rating'] = review.rating
    review_data['movie_id'] = review.movie_id

    return jsonify(review_data)


@bp_open.get('/review/user/<public_id>')
@token_required
def get_review_by_user_public_id(current_user, public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user.reviews:
        return jsonify({'message': 'No reviews found'})

    if not user:
        return jsonify({'message': 'User not found'})

    output = []
    for review in user.reviews:
        review_data = {}
        review_data['id'] = review.id
        review_data['text'] = review.text
        review_data['rating'] = review.rating
        review_data['movie_id'] = review.movie_id
        output.append(review_data)

    return jsonify({f'Reviews by user with public_id: {public_id}': output})


@bp_open.get('review/movie/<movie_id>')
@token_required
def get_reviews_by_movie_id(current_user, movie_id):
    movie = Movie.query.filter_by(movie_id=movie_id).first()
    print(movie)
    output = []

    for review in movie.reviews:
        review_data = {}
        review_data['id'] = review.id
        review_data['text'] = review.text
        review_data['rating'] = review.rating
        review_data['movie_id'] = review.movie_id
        output.append(review_data)
    return jsonify({f'Reviews for movie with id: {movie_id}': output})


@bp_open.post('/review')
@token_required
def create_review(current_user):
    data = request.get_json()
    new_review = Review(text=data['text'], rating=data['rating'], movie_id=data['movie_id'], user_id=current_user.id)
    from app import db
    db.session.add(new_review)
    db.session.commit()

    return jsonify({'message': 'Review added!'})


@bp_open.put('/review/setrating/<review_id>')
@token_required
def set_rating(current_user, review_id):
    data = request.get_json()
    review = Review.query.filter_by(id=review_id).first()

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
        return jsonify({'message': 'Nothing here to delete.'})

    from app import db
    db.session.delete(review)
    db.session.commit()


    return jsonify({'message': f'Review with id {review_id} deleted'})
