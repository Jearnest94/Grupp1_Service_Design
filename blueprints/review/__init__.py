from flask import Blueprint

from blueprints.open import token_required
from models import Review
from flask import request, jsonify

bp_review = Blueprint('bp_review', __name__)


@bp_review.get('/review')
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


@bp_review.get('/review/<review_id>')
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


@bp_review.get('/review/user/<public_id>')
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


@bp_review.get('review/movie/<movie_id>')
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


@bp_review.post('/review')
@token_required
def create_review(current_user):
    data = request.get_json()
    new_review = Review(text=data['text'], rating=data['rating'], movie_id=data['movie_id'], user_id=current_user.id)
    from app import db
    db.session.add(new_review)
    db.session.commit()
