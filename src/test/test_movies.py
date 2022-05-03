"""
Unit tests for movie endpoint
"""

import json
import jsonpath
from .fixture import client

def test_get_movie_status_code(client):
    """
    Test the HTTP status code
    :param client: App test client from fixture
    :return: None
    """
    response = client.get('/api/v1.0/movie')
    assert response.status_code == 200

def test_get_movies(client):
    """
    Test retrieval of movie
    :param client: App test client from fixture
    :return: None
    """
    response = client.get('/api/v1.0/movie')
    data = json.loads(response.text)
    test = data['movie']
    first_film = next((item for item in test if item['movie_id'] == 1), None)
    assert first_film["Series_Title"] == "The Shawshank Redemption"

def test_post_movie(client):
    pass


