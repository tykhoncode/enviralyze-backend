import pytest
from django.contrib.auth import get_user_model
from django.test import Client

pytestmark = pytest.mark.django_db

ADMIN_CHANGELISTS = [
    "/admin/lists/list/",
    "/admin/products/product/",
    "/admin/products/userproductinteraction/",
    "/admin/profiles/profile/",
    "/admin/profiles/follow/",
    "/admin/comments/comment/",
]


@pytest.fixture
def staff_client(settings):
    settings.STORAGES = {
        **settings.STORAGES,
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
    admin = get_user_model().objects.create_user(email="admin@test.com", password="pass12345")
    admin.is_staff = True
    admin.is_superuser = True
    admin.save()
    client = Client()
    client.force_login(admin)
    return client


@pytest.mark.parametrize("url", ADMIN_CHANGELISTS)
def test_admin_changelist_loads(staff_client, url):
    resp = staff_client.get(url)
    assert resp.status_code == 200
