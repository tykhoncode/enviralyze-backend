import pytest
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from lists.models import List
from comments.models import Comment

U = get_user_model()


@pytest.mark.django_db
def test_comment_on_commentable_list(auth_client, user):
    lst = List.objects.create(owner=user, name="L1", type="custom", is_commentable=True)
    resp = auth_client.post(f"/api/lists/{lst.pk}/comments/", {"text": "hi"}, format="json")
    assert resp.status_code == 201
    assert resp.json()["text"] == "hi"


@pytest.mark.django_db
def test_comment_blocked_when_not_commentable(auth_client, user):
    lst = List.objects.create(owner=user, name="L2", type="custom", is_commentable=False)
    resp = auth_client.post(f"/api/lists/{lst.pk}/comments/", {"text": "hi"}, format="json")
    assert resp.status_code == 403


@pytest.mark.django_db
def test_read_list_comments_allowed_even_when_locked(auth_client, user):
    lst = List.objects.create(owner=user, name="L3", type="custom", is_commentable=False)
    Comment.objects.create(
        author=user, text="seed",
        content_type=ContentType.objects.get_for_model(List), object_id=lst.id,
    )
    resp = auth_client.get(f"/api/lists/{lst.pk}/comments/")
    assert resp.status_code == 200
    assert len(resp.json()) == 1
