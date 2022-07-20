import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticate_user(api_client): # api_client is a fixture
    def do_authenticate(is_staff=False): # Now passing the kwargs to be passed to the user object
        api_client.force_authenticate(user=User(is_staff=is_staff))
    return do_authenticate
