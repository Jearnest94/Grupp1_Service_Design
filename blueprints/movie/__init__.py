"""
Bla bla bla
"""

from flask import Blueprint

from models import Movie
from flask import Flask, request, jsonify, make_response

bp_movie = Blueprint('bp_movie', __name__)

@bp_movie.get('/movie')
def get_all_movies():
    movies = Movie.query.all()

    output = []
    for movie in movies:
        movie_data = {}
        movie_data['movie_id'] = movie.movie_id
        movie_data['Series_Title'] = movie.Series_Title
        movie_data['Released_Year'] = movie.Released_Year
        movie_data['Runtime'] = movie.Runtime
        movie_data['Genre'] = movie.Genre
        movie_data['IMDB_Rating'] = movie.IMDB_Rating
        movie_data['Overview'] = movie.Overview
        movie_data['Director'] = movie.Director
        movie_data['Star1'] = movie.Star1

        output.append(movie_data)
    return jsonify({'movie': output}), 200


@bp_movie.post('/movie')
def create_movie():
    data = request.get_json()

    new_movie = Movie(Series_Title=data['Series_Title'], Released_Year=data['Released_Year'], Runtime=data['Runtime'], Genre=data['Genre'], IMDB_Rating=data['IMDB_Rating'], Overview=data['Overview'], Director=data['Director'], Star1=data['Star1'])
    from app import db
    db.session.add(new_movie)
    db.session.commit()
    return jsonify({'message': f'The movie {new_movie.Series_Title} with movie_id {new_movie.movie_id} added!'}), 201


@bp_movie.get('/movie/<movie_id>') #Vad ska jag ha för värde här?
def get_one_movie(movie_id):

    movie = Movie.query.filter_by(movie_id=movie_id).first()
    if not movie:
        return jsonify({'message': f'Movie with movie_id {movie_id} not found!'}), 404

    movie_data = {}
    movie_data['movie_id'] = movie.movie_id
    movie_data['Series_Title'] = movie.Series_Title
    movie_data['Released_Year'] = movie.Released_Year
    movie_data['Runtime'] = movie.Runtime
    movie_data['Genre'] = movie.Genre
    movie_data['IMDB_Rating'] = movie.IMDB_Rating
    movie_data['Overview'] = movie.Overview
    movie_data['Director'] = movie.Director
    movie_data['Star1'] = movie.Star1

    return jsonify({'movie': movie_data}), 200


@bp_movie.put('/movie/<movie_id>') #Vad ska jag ha för värde här?
def alter_movie_details(movie_id):

    movie = Movie.query.filter_by(movie_id=movie_id).first()
    if not movie:
        return jsonify({f'message': 'Movie not found!'}), 404

    data = request.get_json()
    new_movie = Movie(Series_Title=data['Series_Title'], Released_Year=data['Released_Year'], Runtime=data['Runtime'], Genre=data['Genre'], IMDB_Rating=data['IMDB_Rating'], Overview=data['Overview'], Director=data['Director'], Star1=data['Star1'])

    movie.update(new_movie)

    from app import db
    db.session.commit()
    return jsonify({'message': f'The movie {movie.Series_Title} with movie_id {movie.movie_id} updated!'}), 200


@bp_movie.delete('/movie/<movie_id>')
def delete_movie(movie_id):
    movie = Movie.query.filter_by(movie_id=movie_id).first()
    if not movie:
        return jsonify({"message": f'{movie.Series_Title} with movie_id {movie.movie_id} not found!'}), 404

    from app import db
    db.session.delete(movie)
    db.session.commit()

    return jsonify({"message": f'The movie {movie.Series_Title} with movie_id {movie.movie_id} deleted!'}), 200





