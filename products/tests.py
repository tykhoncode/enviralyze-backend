import pytest
from django.contrib.auth import get_user_model
from products.models import Product, UserProductInteraction

U = get_user_model()


@pytest.mark.django_db
def test_my_votes_splits_approved_disapproved(auth_client, user):
    p1 = Product.objects.create(barcode="12345678", name="Approved One")
    p2 = Product.objects.create(barcode="87654321", name="Disapproved One")
    UserProductInteraction.objects.create(user=user, product=p1, approved=True)
    UserProductInteraction.objects.create(user=user, product=p2, approved=False)
    resp = auth_client.get("/api/products/my-votes/")
    assert resp.status_code == 200
    data = resp.json()
    assert [p["barcode"] for p in data["approved"]] == ["12345678"]
    assert [p["barcode"] for p in data["disapproved"]] == ["87654321"]


@pytest.mark.django_db
def test_my_votes_requires_auth(api_client):
    resp = api_client.get("/api/products/my-votes/")
    assert resp.status_code == 401
