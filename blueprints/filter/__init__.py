from flask import Blueprint, request, jsonify, Response

from models import Movie

blueprint = Blueprint('blueprint', __name__)

@blueprint.route('/rating/<float:rating>')
def get_movies_by_Rating(rating):
    movies = Movie.query.filter_by(IMDB_Rating=rating).all()

    print(movies)

    output = []
    for movie in movies:
        movie_data = {}
        movie_data['movie_id'] = movie.movie_id
        movie_data['Poster_Link'] = movie.Poster_Link
        movie_data['Series_Title'] = movie.Series_Title
        movie_data['Released_Year'] = movie.Released_Year
        movie_data['Certificate'] = movie.Certificate
        movie_data['Runtime'] = movie.Runtime
        movie_data['Genre'] = movie.Genre
        movie_data['IMDB_Rating'] = movie.IMDB_Rating
        movie_data['Overview'] = movie.Overview
        movie_data['Meta_score'] = movie.Meta_score
        movie_data['Director'] = movie.Director
        movie_data['Star1'] = movie.Star1
        movie_data['Star2'] = movie.Star2
        movie_data['Star3'] = movie.Star3
        movie_data['Star4'] = movie.Star4
        movie_data['No_of_Votes'] = movie.No_of_Votes
        movie_data['Gross'] = movie.Gross

        output.append(movie_data)
    return jsonify({'movie': output})


@blueprint.route('/year/<int:year>')
def get_movies_by_Year(year):
    movies = Movie.query.filter_by(Released_Year=year).all()

    print(movies)

    output = []
    for movie in movies:
        movie_data = {}
        movie_data['movie_id'] = movie.movie_id
        movie_data['Poster_Link'] = movie.Poster_Link
        movie_data['Series_Title'] = movie.Series_Title
        movie_data['Released_Year'] = movie.Released_Year
        movie_data['Certificate'] = movie.Certificate
        movie_data['Runtime'] = movie.Runtime
        movie_data['Genre'] = movie.Genre
        movie_data['IMDB_Rating'] = movie.IMDB_Rating
        movie_data['Overview'] = movie.Overview
        movie_data['Meta_score'] = movie.Meta_score
        movie_data['Director'] = movie.Director
        movie_data['Star1'] = movie.Star1
        movie_data['Star2'] = movie.Star2
        movie_data['Star3'] = movie.Star3
        movie_data['Star4'] = movie.Star4
        movie_data['No_of_Votes'] = movie.No_of_Votes
        movie_data['Gross'] = movie.Gross

        output.append(movie_data)
    return jsonify({'movie': output})


@blueprint.route('/director/<director>')
def get_movies_by_Director(director):
    movies = Movie.query.filter_by(Director=director).all()

    print(movies)

    output = []
    for movie in movies:
        movie_data = {}
        movie_data['movie_id'] = movie.movie_id
        movie_data['Poster_Link'] = movie.Poster_Link
        movie_data['Series_Title'] = movie.Series_Title
        movie_data['Released_Year'] = movie.Released_Year
        movie_data['Certificate'] = movie.Certificate
        movie_data['Runtime'] = movie.Runtime
        movie_data['Genre'] = movie.Genre
        movie_data['IMDB_Rating'] = movie.IMDB_Rating
        movie_data['Overview'] = movie.Overview
        movie_data['Meta_score'] = movie.Meta_score
        movie_data['Director'] = movie.Director
        movie_data['Star1'] = movie.Star1
        movie_data['Star2'] = movie.Star2
        movie_data['Star3'] = movie.Star3
        movie_data['Star4'] = movie.Star4
        movie_data['No_of_Votes'] = movie.No_of_Votes
        movie_data['Gross'] = movie.Gross

        output.append(movie_data)
    return jsonify({'movie': output})