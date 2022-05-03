import json

import pandas as pd
from flask import Blueprint, request, jsonify, Response

from models import Movie


blueprint = Blueprint('blueprint', __name__)


# @blueprint.route('/get')
# def get():
#     data = pd.read_csv('imdb_top_1000.csv')
#     data = data.to_dict('records')
#     # print({'data': data}, 200)
#     return {'data': data}


# @blueprint.route('/movie/rating')
# def get():
#     fields = ['Series_Title', 'IMDB_Rating']
#
#     data = pd.read_csv('imdb_top_1000', skipinitialspace=True, usecols=fields)
#     data = data.to_dict('records')
#
#     return {'data': data}, 200


# CREATE MORE: Text = <username>, num =<int:id>
# @blueprint.route("/movie/rating/<float:rate>")
# def get(rate):
#
#     num_rate = rate
#
#     data = pd.read_csv('imdb_top_1000.csv')
#
#     data_new = data[data["IMDB_Rating"] == num_rate]
#
#     data_new = data_new.to_dict('records')
#
#     return {'data': data_new}, 200
#
#

@blueprint.route('/api/v1.0/Rating/<float:Rating>')
def get_all_movies(Rating):

    movies = Movie.query.filter_by(IMDB_Rating=Rating).all()

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


# @blueprint.route('/')
# def get():
#     return 'Hello, World!'
#
#
# @blueprint.route('/hello')
# def configure_routes():
#     return 'Hello, World!'

# @blueprint.route('/get')
# def second_get():
#
#     return 'Hello, World!'
#     # return Response(json.dumps(data), 200, content_type='application/json')