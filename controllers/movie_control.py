"""
Controllers for movies
"""

def get_all_movies():
    from models import Movie
    return Movie.query.all()
