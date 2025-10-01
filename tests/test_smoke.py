import pytest

pytestmark = pytest.mark.django_db

def test_db_fixture(user):
    assert user.pk is not None

def test_health(api_client):
    res = api_client.get("/api/health/")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}

def test_lists_endpoint_no_500(api_client):
    res = api_client.get("/api/lists/")
    assert res.status_code in (200, 401, 403)