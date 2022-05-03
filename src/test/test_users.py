# from flask import Flask
# import json
#
# from blueprints.filter import get, configure_routes


# def test_base_route():
#     app = Flask(__name__)
#     configure_routes(app)
#     client = app.test_client()
#     url = '/hello'
#
#     response = client.get(url)
#     # assert response.get_data() == b'Hello, World!'
#     # assert response.get_data() ==
#     assert response.status_code == 200

from .fixture import client


def test_Rating_status_code(client):
    response = client.get('/api/v1.0/Rating/8.6')
    assert response.status_code == 200
    print("Test")


def test_movie_status_code(client):
    response = client.get('/api/v1.0/movie')
    assert response.status_code == 200

# def test_user_status_code(client):
#
#     response = client.get('/user')
#     assert response.status_code == 200
