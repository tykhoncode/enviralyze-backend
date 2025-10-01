import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    return get_user_model().objects.create_user(email="user1@test.com", password="Test1234!")

@pytest.fixture
def another_user(db):
    return get_user_model().objects.create_user(email="stranger@test.com", password="stranger")

@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client