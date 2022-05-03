"""
Unit tests for movie endpoint
"""
import requests
import json
import jsonpath
from .fixture import client

def test_get_movie_status_code(client):
    """
    Test the HTTP status code
    :param client: App test client from fixture
    :return: None
    """
    response = client.get('api/v.1.0/movie')
    assert response.status_code == 200

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
    request = client.post('api/v.1.0/movie')
    data = json.loads(request.text)


    url = 'http://localhost:5000/api/v.1.0/movie'
    obj_to_post = {
        'Series-title': 'Some Title',
        'Released-year': 1987
        # bygg ut med mer
    }
    response = requests.post(url, data=obj_to_post)
    # TODO:
    # Implement movie/<id> - GET
    # Make a get call to movie/<id> with the id you got in the respons
    # Check that it is th same as you posted
    # call movie/<id> - DELETE with the same id to clean things up
    # Make a get call to movie/<id> with the id you got in the respons to make sure it is now deleted
    assert response == None




