from django.db.models.signals import post_save
from django.dispatch import receiver
from core.emails import send_notification_email
from .models import List


@receiver(post_save, sender=List)
def notify_followers_on_new_list(sender, instance, created, **kwargs):
    if not created:
        return
    owner = instance.owner
    owner_profile = getattr(owner, "profile", None)
    if owner_profile is None:
        return
    name = f"{owner.first_name} {owner.last_name}".strip() or owner.email
    for follower_profile in owner_profile.followers.select_related("user").all():
        send_notification_email(
            f"{name} posted a new list on Enviralyze",
            f"{name} just posted a new list '{instance.name}'. Check it out on Enviralyze.",
            follower_profile.user,
        )
