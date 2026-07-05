import pytest
from django.contrib.auth import get_user_model
from profiles.models import Follow
from lists.models import List

U = get_user_model()


@pytest.mark.django_db
def test_new_follower_emails_target(mailoutbox):
    a = U.objects.create_user(email="a@test.com", password="x")
    b = U.objects.create_user(email="b@test.com", password="x")
    Follow.objects.create(follower=a.profile, following=b.profile)
    assert len(mailoutbox) == 1
    assert mailoutbox[0].to == ["b@test.com"]


@pytest.mark.django_db
def test_opt_out_suppresses_follower_email(mailoutbox):
    a = U.objects.create_user(email="a2@test.com", password="x")
    b = U.objects.create_user(email="b2@test.com", password="x")
    b.profile.email_notifications = False
    b.profile.save()
    Follow.objects.create(follower=a.profile, following=b.profile)
    assert mailoutbox == []


@pytest.mark.django_db
def test_new_list_emails_followers(mailoutbox):
    owner = U.objects.create_user(email="owner@test.com", password="x")
    fan = U.objects.create_user(email="fan@test.com", password="x")
    Follow.objects.create(follower=fan.profile, following=owner.profile)
    mailoutbox.clear()
    List.objects.create(owner=owner, name="Eco Picks", type="custom")
    assert [m.to for m in mailoutbox] == [["fan@test.com"]]


@pytest.mark.django_db
def test_me_can_toggle_email_notifications(auth_client, user):
    resp = auth_client.patch("/api/profiles/me/", {"email_notifications": False}, format="json")
    assert resp.status_code == 200
    user.profile.refresh_from_db()
    assert user.profile.email_notifications is False
