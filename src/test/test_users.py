"""
Unit tests for user endpoint
"""
import json

# import flask

from models import User
# , Movie

# from flask import request, jsonify, make_response
# import pytest
# import requests
# from .fixture import client

def test_user_models(client):
    user = User(public_id=6000, name='admin')
    assert user.name == 'admin'


def test_user_status_code(client):
    response = client.get('/api/v1.0/user')
    assert response.status_code == 200
    assert b'test' in response.datadef


def test_user_get_token(client):
    import requests

    url = "http://localhost:5000/api/v1.0/login"
    username = "admin"
    password = "123"
    response = requests.get(url, auth=(username, password))
    print(response.status_code)
    print(response.json())


# def test_user_token(client):
#
#     import requests
#
#     url = "http://localhost:5000/api/v1.0/user"
#     header = {"x-access-token":
#     "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjYwMDAiLCJleHAiOjE2NTIyMjM4MTl9.
#     vUK1_I8K041sZk2YgXmk8sE3Ig828pWnsptifB13fC4"}
#     response = requests.get(url, headers=header)
#     print(response.status_code)
#     print(response.json())

# def test_get_token(client):
#     headers = request.headers.get('x-access-token')
#     bearer = headers.get('Authorization')  # Bearer YourTokenHere
#     token = bearer.split()[1]  # YourTokenHere
#     print(token)


# def test_get_one_user(client):
#     response = client.get('/api/v.1.0/user/6000')
#     assert response.status_code == 200


def test_get_user(client):
    response = client.get('/api/v.1.0/user')
    data = json.loads(response.text)
    test = data['user']
    first_user = next((item for item in test if item['id'] == 6000), None)
    assert first_user["name"] == "admin"


def test_post_and_delete_user(client):
    url = 'http://localhost:5000/api/v.1.0/user'

    obj_to_post = {
        "id": 3,
        "public_id": 3000,
        "name": 'fisk',
        "password": "321",
        "admin": "true",
    }

    # Check that new movie object has been created
    response = client.post(url, json=obj_to_post)
    assert response.status_code == 201

    # Retrieve movie_id from the response
    # data = response.json
    # value = data["message"]
    # numbers = []
    # for word in value.split():
    #     if word.isdigit():
    #         numbers.append(int(word))
    # id = numbers[0000]

    # Update url and check that new movie is in the db
    url = "http://localhost:5000/api/v.1.0/user/3000"

    response2 = client.get(url)
    data = json.loads(response2.text)
    User_data = data['user']
    assert User_data["id"] == 3000
    assert User_data["name"] == "fisk"

    # Delete
    response3 = client.delete(url)
    assert response3.status_code == 200

    response4 = client.get(url)
    assert response4.status_code == 404
