import pytest
from lists.models import List

pytestmark = pytest.mark.django_db


# --- CREATE ---

def test_guest_cannot_create_list(api_client):
    res = api_client.post("/api/lists/", {"name": "Groceries"}, format="json")
    assert res.status_code in (401, 403)


def test_auth_can_create_list(auth_client, user):
    res = auth_client.post("/api/lists/", {"name": "Groceries"}, format="json")
    assert res.status_code == 201
    lst = List.objects.get(id=res.data["id"])
    assert lst.owner == user
    assert lst.name == "Groceries"
    assert lst.is_public is False  # default


def test_create_list_without_name_fails(auth_client):
    res = auth_client.post("/api/lists/", {"is_public": True}, format="json")
    assert res.status_code == 400
    assert "name" in res.data


def test_create_list_with_empty_name_fails(auth_client):
    res = auth_client.post("/api/lists/", {"name": "", "is_public": True}, format="json")
    assert res.status_code == 400


def test_create_list_with_long_name_fails(auth_client):
    long_name = "A" * 300
    res = auth_client.post("/api/lists/", {"name": long_name}, format="json")
    assert res.status_code == 400


def test_owner_cannot_be_overwritten(auth_client, another_user):
    res = auth_client.post("/api/lists/", {
        "name": "Hack",
        "owner": another_user.id
    }, format="json")
    assert res.status_code == 201
    assert res.data["owner"] != another_user.id


# --- RETRIEVE ---

def test_auth_can_retrieve_own_list(auth_client, user):
    lst = List.objects.create(name="My List", owner=user, is_public=False)
    res = auth_client.get(f"/api/lists/{lst.id}/")
    assert res.status_code == 200
    assert res.data["name"] == "My List"


def test_auth_can_retrieve_public_list_of_other(auth_client, another_user):
    lst = List.objects.create(name="Public Stuff", owner=another_user, is_public=True)
    res = auth_client.get(f"/api/lists/{lst.id}/")
    assert res.status_code == 200
    assert res.data["name"] == "Public Stuff"


def test_auth_cannot_retrieve_private_list_of_other(auth_client, another_user):
    lst = List.objects.create(name="Private Stuff", owner=another_user, is_public=False)
    res = auth_client.get(f"/api/lists/{lst.id}/")
    assert res.status_code in (403, 404)


# --- UPDATE ---

def test_auth_can_update_own_list(auth_client, user):
    lst = List.objects.create(name="Old Name", owner=user, is_public=False)
    res = auth_client.patch(f"/api/lists/{lst.id}/", {"name": "New Name"}, format="json")
    assert res.status_code == 200
    lst.refresh_from_db()
    assert lst.name == "New Name"


def test_auth_cannot_update_private_list_of_other(auth_client, another_user):
    lst = List.objects.create(name="Secret", owner=another_user, is_public=False)
    res = auth_client.patch(f"/api/lists/{lst.id}/", {"name": "Hack"}, format="json")
    assert res.status_code in (403, 404)


# --- DELETE ---

def test_auth_can_delete_own_list(auth_client, user):
    lst = List.objects.create(name="Trash", owner=user)
    res = auth_client.delete(f"/api/lists/{lst.id}/")
    assert res.status_code in (200, 204)
    assert not List.objects.filter(id=lst.id).exists()


def test_auth_cannot_delete_list_of_other(auth_client, another_user):
    lst = List.objects.create(name="Not Yours", owner=another_user)
    res = auth_client.delete(f"/api/lists/{lst.id}/")
    assert res.status_code in (403, 404)
    assert List.objects.filter(id=lst.id).exists()