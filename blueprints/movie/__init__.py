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
    return jsonify({'movie': output})

@bp_movie.post('/movie')
def create_movie():
    series_title = request.get_json() #Vad ska jag hämta här?
    released_year = request.get_json()
    runtime = request.get_json()
    genre = request.get_json()
    imdb_rating = request.get_json()
    overview = request.get_json()
    director = request.get_json()
    star1 = request.get_json()
    new_movie = Movie(Series_Title=series_title, Released_Year=released_year, Runtime=runtime, Genre=genre, IMDB_Rating=imdb_rating, Overview=overview, Director=director, Star1=star1)
    from app import db
    db.session.add(new_movie)
    db.session.commit()
    return jsonify({f'message': 'Movie' + series_title + 'added!'})

@bp_movie.put('/movie/<series_title>') #Vad ska jag ha för värde här?
def alter_movie_details(series_title):

    movie = Movie.query.filter_by(Series_Title=series_title).first()

    if not movie:
        return jsonify({f'message': 'Movie' + series_title + 'not found!'})

    # Hur gör jag här?


@bp_movie.delete('/movie/<series_title>')
def delete_movie(series_title):
    movie = Movie.query.filter_by(Series_Title=series_title).first()
    if not movie:
        return jsonify({"message": "The movie" + series_title + "not found!"})

    # GAAAAAAAAHHHH

    from app import db
    db.session.delete(movie)
    db.session.commit()

    return jsonify({f"message": "The movie" + series_title + "has been deleted!"})





