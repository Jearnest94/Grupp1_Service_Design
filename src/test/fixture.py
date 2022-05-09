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
    def __init__(self, client):
        self._client = client

    def login(self, username='admin', password='123'):
        return self._client.post(
            '/api/v1.0/login',
            data={'username': username, 'password': password})

    # Har vi en sådan endpoint?
    def logout(self):
        return self._client.get('/api/v1.0/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
