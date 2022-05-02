"""
Unit tests for movie endpoint
"""

import json
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

    # GAAAAHHHHHH

