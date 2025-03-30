from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import MyList

@receiver(post_save, sender=User)
def create_default_lists(sender, instance, created, **kwargs):
    """
        When a new user is created, create default lists for them.
    """
    if created:
        default_names = ["Favorites", "Watched", "Recommended"]
        for name in default_names:
            MyList.objects.create(
                user=instance,
                name=name
            )