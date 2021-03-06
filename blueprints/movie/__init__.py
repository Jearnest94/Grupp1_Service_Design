"""
CRUD for endpoint movie
"""
import datetime

from flask import request, jsonify, Blueprint
from models import Movie, User, Log

from app import db

bp_movie = Blueprint('bp_movie', __name__)


@bp_movie.get('/movie')
def get_all_movies():
    """
    :return: return all the movies in the database
    """

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
        movie_data['links'] = {
            'All reviews for this movie': f'/api/v1.0/review/movie/{movie.movie_id}',
            'This movie': f'/api/v1.0/movie/{movie.movie_id}'
        }

        output.append(movie_data)
    return jsonify({'movie': output}), 200


@bp_movie.post('/movie')
def create_movie():
    """
    :return: creates a new movie
    """

    data = request.get_json()
    new_movie = Movie(Series_Title=data['Series_Title'], Released_Year=data['Released_Year'],
                      Runtime=data['Runtime'], Genre=data['Genre'], IMDB_Rating=data['IMDB_Rating'],
                      Overview=data['Overview'], Director=data['Director'], Star1=data['Star1'])

    db.session.add(new_movie)
    db.session.commit()
    last_added_movie = Movie.query.order_by(Movie.id.desc()).first()
    return jsonify({'message': f'The movie {new_movie.Series_Title} '
                               f'with movie_id {new_movie.movie_id} added!',
                    'This movie': f'/api/v1.0/movie/{last_added_movie.id}',
                    'All movies': "/api/v1.0/movie"}), 201


@bp_movie.get('/movie/<movie_id>')
def get_one_movie(movie_id):
    """
    :param movie_id: finds the move with that movie_id
    :return: returns that movie with that movie_id
    """

    movie = Movie.query.filter_by(movie_id=movie_id).first()

    if not movie:
        return jsonify({'message': f'Movie with movie_id {movie_id} not found!',
                        'All movies': "api/v1.0/movie"}), 404

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
    movie_data['links'] = {
        'All movies': '/api/v1.0/movie',
        'All reviews for this movie': f'/api/v1.0/review/movie/{movie.movie_id}'
    }

    return jsonify({'movie': movie_data}), 200


@bp_movie.put('/movie/<movie_id>')
def alter_movie_details(movie_id):
    """
    :param movie_id: gets the movie with that movie_id
    :return: returns the movie with the altered data
    """
    movie = Movie.query.filter_by(movie_id=movie_id).first()
    if not movie:
        return jsonify({'message': 'Movie not found!', 'All movies': "/api/v1.0/movie"}), 404

    data = request.get_json()
    new_movie = Movie(Series_Title=data['Series_Title'], Released_Year=data['Released_Year'],
                      Runtime=data['Runtime'], Genre=data['Genre'], IMDB_Rating=data['IMDB_Rating'],
                      Overview=data['Overview'], Director=data['Director'], Star1=data['Star1'])

    movie.update(new_movie)

    db.session.commit()

    return jsonify({'message': f'The movie {movie.Series_Title} with movie_id {movie.movie_id} '
                               f''f'updated!', 'This movie': f'/api/v1.0/movie/{movie.movie_id}',
                    'All movies': "/api/v1.0/movie"}), 202


@bp_movie.delete('/movie/<movie_id>')
def delete_movie(movie_id):
    """
    :param movie_id: gets the movie with the movie_id
    :return: deletes that movie
    """

    movie = Movie.query.filter_by(movie_id=movie_id).first()
    if not movie:
        return jsonify({'message': f'{movie.Series_Title} with movie_id '
                                   f'{movie.movie_id} not found!',
                        'All movies': "/api/v1.0/movie"}), 404

    db.session.delete(movie)
    db.session.commit()
    return jsonify({'message': f'The movie {movie.Series_Title} with movie_id '
                               f'{movie.movie_id} deleted!', 'All movies': "/api/v1.0/movie"}), 200


@bp_movie.get('movie/rating/<float:rating>')
def get_movies_by_rating(rating):
    """
    :param rating: get all the movies with that rating
    :type float
    :return: printing out all the movies with that rating
    """

    movies = Movie.query.filter_by(IMDB_Rating=rating).all()
    if not movies:
        return jsonify({'message': f'No movies with rating {rating} found',
                        'All movies': "/api/v1.0/movie"}), 404

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
    return jsonify({f'Movies rated {rating}': output}), 200


@bp_movie.get('movie/year/<int:year>')
def get_movies_by_year(year):
    """
    :param year: get all the movies with that was made that year
    :return: print out all the movies with that year
    """

    movies = Movie.query.filter_by(Released_Year=year).all()
    if not movies:
        return jsonify({'message': f'No movies released year {year} found',
                        'All movies': "/api/v1.0/movie"}), 404

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
    return jsonify({f'Movies released {year}': output}), 200


@bp_movie.get('movie/director/<director>')
def get_movies_by_director(director):
    """

    :param director: get all the movies with that director
    :return: prints out all movies with that director
    """

    movies = Movie.query.filter_by(Director=director).all()
    if not movies:
        return jsonify({'message': f'No movies directed by {director} found',
                        'All movies': "/api/v1.0/movie"}), 404

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
    return jsonify({f'Movies directed by {director}': output}), 200


@bp_movie.before_request
def logger():
    """
    :return: Logs API Activity into log table in database
    """
    token = request.headers.get('x-access-token')
    user = User.query.filter_by(latesttoken=token).first()
    now = datetime.datetime.utcnow()
    new_log = Log(user=user.name, endpoint=request.endpoint, timestamp=now)
    db.session.add(new_log)
    db.session.commit()
    print(f'API Accessed - User: {user.name} - Endpoint: {request.endpoint} '
          f'\t {now.strftime("%Y-%m-%d %H:%M:%S")}')
