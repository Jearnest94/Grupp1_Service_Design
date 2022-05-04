"""
Unit tests for movie endpoint
"""
import requests
import json

from models import Movie
from .fixture import client

def test_movie_models():
    movie = Movie(Series_Title='New Film', Released_Year=1988, Runtime='100 min', Genre='Romantic comedy', IMDB_Rating=7.0, Overview='A good movie', Director='Colin Nutley', Star1='Helena Bergström')
    assert movie.Star1 == 'Helena Bergström'


def test_get_movie_status_code(client):
    """
    Test the HTTP status code
    :param client: App test client from fixture
    :return: None
    """
    response = client.get('api/v.1.0/movie')
    assert response.status_code == 200
    assert b'12 Angry Men' in response.data

def test_get_movies(client):
    """
    Test retrieval of movie
    :param client: App test client from fixture
    :return: None
    """
    response = client.get('/api/v.1.0/movie')
    data = json.loads(response.text)
    test = data['movie']
    first_film = next((item for item in test if item['movie_id'] == 1), None)
    assert first_film["Series_Title"] == "The Shawshank Redemption"

def test_post_movie(client):

    url = 'http://localhost:5000/api/v.1.0/movie'

    obj_to_post = {
        "Series_Title": "Test Film",
        "Released_Year": 1987,
        "Runtime": "120 min",
        "Genre": "Gastro-Thriller",
        "IMDB_Rating": 8.5,
        "Overview": "This is a test",
        "Director": "Test Testsson",
        "Star1": "Nicholas Cage"
    }

    #response = requests.post(url, data=obj_to_post)

    response = client.post(url, json=obj_to_post)
    assert response.status_code == 201
    data = response.json
    value = data["message"]
    numbers = []
    for word in value.split():
        if word.isdigit():
            numbers.append(int(word))
    movie_id = numbers[0]
    response = client.get(f'api/v.1.0/movie/{movie_id}') # Skapa denna funktion
    print(movie_id)

    # Hur hämtar jag ut movie_id?

    #response = client.post('/api/v.1.0/movie', data=obj_to_post)
    #from app import db
    #db.session.add(new_movie)
    #db.session.commit()
    #print(movie_post)
    #assert response.data[''] in response.data
    #print(response['data'])

    #assert response[124] == b'Test Film'

    #client.post('/api/v.1.0/movie', data=obj_to_post)

    # with app.app_context():
    # TODO:


    # Implement movie/<id> - GET
    # Make a get call to movie/<id> with the id you got in the response
    # Check that it is th same as you posted
    # call movie/<id> - DELETE with the same id to clean things up
    # Make a get call to movie/<id> with the id you got in the respons to make sure it is now deleted





    #assert response == None

# movie = Movie.query.filter_by(Series_Title="Test Film").first()


