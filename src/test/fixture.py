"""
Fixture for tests
"""

import pytest
from app import create_app


@pytest.fixture
def client():
    """
    Test fixture for api client
    :return: yields a test client
    """
    app = create_app()

    app.config['TESTING'] = True

    with app.app_context():
        with app.test_client() as api_client:
            yield api_client

# Osäker på om denna funkar, lägg till metoden
# auth.login()
# i test för att logga in som testanvändaren

class AuthActions(object):
    """
    Authentication
    """
    def __init__(self, client):
        """
        Returns client
        :param client: Client
        """
        self._client = client

    def login(self, username='admin', password='123'):
        """
        Login func
        :param username: admin
        :param password: 123
        :return: data
        """
        return self._client.post(
            '/api/v1.0/login',
            data={'username': username, 'password': password})


@pytest.fixture
def auth(client):
    """

    :param client:
    :return:
    """
    return AuthActions(client)

