"""
Unit tests for movie endpoint
"""

import json
from models import Movie
from .fixture import client


def test_movie_models(client):
    """
    Test movie models
    :param client: App test client from fixture
    :return: None
    """
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
    Test retrieval of movies
    :param client: App test client from fixture
    :return: None
    """
    response = client.get('/api/v.1.0/movie')
    data = json.loads(response.text)
    test = data['movie']
    first_film = next((item for item in test if item['movie_id'] == 1), None)
    assert first_film["Series_Title"] == "The Shawshank Redemption"

def test_post_and_delete_movie(client):
    """
    Test post of new movie object, response code, get new movie from db, then delete.
    :param client: App test client from fixture
    :return: None
    """
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

    # Check that new movie object has been created
    response = client.post(url, json=obj_to_post)
    assert response.status_code == 201

    # Retrieve movie_id from the response
    data = response.json
    value = data["message"]
    numbers = []
    for word in value.split():
        if word.isdigit():
            numbers.append(int(word))
    movie_id = numbers[0]

    # Update url and check that new movie is in the db
    url = f'http://localhost:5000/api/v.1.0/movie/{movie_id}'

    response2 = client.get(url)
    data = json.loads(response2.text)
    film = data['movie']
    assert film["Series_Title"] == "Test Film"
    assert film["Star1"] == "Nicholas Cage"

    # Delete
    response3 = client.delete(url)
    assert response3.status_code == 200

    response4 = client.get(url)
    assert response4.status_code == 404
