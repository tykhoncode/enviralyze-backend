import pytest
from django.contrib.auth import get_user_model
from lists.models import List


pytestmark = pytest.mark.django_db


def test_guest_can_see_public_list(api_client, user):
    lst = List.objects.create(name="Public List", owner=user, is_public=True)
    res = api_client.get(f"/api/lists/{lst.id}/")
    assert res.status_code == 200
    assert res.data["name"] == "Public List"


def test_guest_cannot_see_private_list(api_client, user):
    lst = List.objects.create(name="Private List", owner=user, is_public=False)
    res = api_client.get(f"/api/lists/{lst.id}/")
    assert res.status_code in (403, 404)


def test_stranger_cannot_see_private_list(auth_client, user, another_user):
    lst = List.objects.create(name="Private List", owner=user, is_public=False)
    auth_client.force_authenticate(user=another_user)
    res = auth_client.get(f"/api/lists/{lst.id}/")
    assert res.status_code in (403, 404)


def test_stranger_cannot_update_or_delete_list(auth_client, user, another_user):
    lst = List.objects.create(name="Private List", owner=user, is_public=True)
    auth_client.force_authenticate(user=another_user)

    res_update = auth_client.patch(f"/api/lists/{lst.id}/", {"name": "Hack!"})
    res_delete = auth_client.delete(f"/api/lists/{lst.id}/")

    assert res_update.status_code in (403, 404)
    assert res_delete.status_code in (403, 404)
    assert List.objects.filter(id=lst.id).exists()