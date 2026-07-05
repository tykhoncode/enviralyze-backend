import pytest
from lists.models import List
from products.models import Product

pytestmark = pytest.mark.django_db


def test_cannot_read_items_of_others_private_list(auth_client, another_user):
    lst = List.objects.create(owner=another_user, name="P", type="custom", is_public=False)
    res = auth_client.get(f"/api/lists/{lst.pk}/products/")
    assert res.status_code == 404


def test_can_read_items_of_others_public_list(auth_client, another_user):
    lst = List.objects.create(owner=another_user, name="Pub", type="custom", is_public=True)
    res = auth_client.get(f"/api/lists/{lst.pk}/products/")
    assert res.status_code == 200


def test_cannot_add_product_to_others_public_list(auth_client, another_user):
    lst = List.objects.create(owner=another_user, name="Pub2", type="custom", is_public=True)
    prod = Product.objects.create(barcode="11112222", name="X")
    res = auth_client.post(f"/api/lists/{lst.pk}/products/", {"product": prod.id}, format="json")
    assert res.status_code == 403


def test_cannot_add_product_to_others_private_list(auth_client, another_user):
    lst = List.objects.create(owner=another_user, name="Priv2", type="custom", is_public=False)
    prod = Product.objects.create(barcode="22223333", name="Z")
    res = auth_client.post(f"/api/lists/{lst.pk}/products/", {"product": prod.id}, format="json")
    assert res.status_code == 404


def test_can_add_product_to_own_list(auth_client, user):
    lst = List.objects.create(owner=user, name="Mine", type="custom")
    prod = Product.objects.create(barcode="33334444", name="Y")
    res = auth_client.post(f"/api/lists/{lst.pk}/products/", {"product": prod.id}, format="json")
    assert res.status_code == 201
