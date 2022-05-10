from flask import Blueprint

from controllers.user_control import token_required
from models import Review, Movie, User
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

    return jsonify({'reviews': output}), 200


@bp_review.get('/review/<review_id>')
@token_required
def get_one_review(current_user, review_id):
    review = Review.query.filter_by(id=review_id).first()

    if not review:
        return jsonify({'message': 'No review found'}), 404

    review_data = {}
    review_data['id'] = review.id
    review_data['text'] = review.text
    review_data['rating'] = review.rating
    review_data['movie_id'] = review.movie_id

    return jsonify(review_data), 200


@bp_review.get('/review/user/<id>')
@token_required
def get_review_by_user_id(current_user, id):
    user = User.query.filter_by(id=id).first()

    if not user.reviews:
        return jsonify({'message': 'No reviews found'}), 404

    if not user:
        return jsonify({'message': 'User not found'}), 404

    output = []
    for review in user.reviews:
        review_data = {}
        review_data['id'] = review.id
        review_data['text'] = review.text
        review_data['rating'] = review.rating
        review_data['movie_id'] = review.movie_id
        output.append(review_data)

    return jsonify({f'Reviews by user with id: {id}': output}), 200


@bp_review.get('review/movie/<movie_id>')
@token_required
def get_reviews_by_movie_id(current_user, movie_id):
    movie = Movie.query.filter_by(movie_id=movie_id).first()
    output = []

    for review in movie.reviews:
        review_data = {}
        review_data['id'] = review.id
        review_data['text'] = review.text
        review_data['rating'] = review.rating
        review_data['movie_id'] = review.movie_id
        output.append(review_data)
    return jsonify({f'Reviews for movie with id: {movie_id}': output}), 200


@bp_review.post('/review')
@token_required
def create_review(current_user):
    data = request.get_json()
    new_review = Review(text=data['text'], rating=data['rating'], movie_id=data['movie_id'], user_id=current_user.id)
    from app import db
    db.session.add(new_review)
    db.session.commit()

    return jsonify({'message': 'Review added!'}), 201


@bp_review.put('/review/setrating/<review_id>')
@token_required
def set_rating(current_user, review_id):
    data = request.get_json()
    review = Review.query.filter_by(id=review_id).first()

    if not review:
        return jsonify({'message': 'No review found'}), 404

    review.rating = data['rating']
    from app import db
    db.session.commit()

    return jsonify({'message': 'Rating adjusted.'}), 200


@bp_review.delete('/review/<review_id>')
@token_required
def delete_review(current_user, review_id):
    review = Review.query.filter_by(id=review_id, user_id=current_user.id).first()

    if not review:
        return jsonify({'message': 'Nothing here to delete.'}), 404

    from app import db
    db.session.delete(review)
    db.session.commit()

    return jsonify({'message': f'Review with id {review_id} deleted'}), 200

