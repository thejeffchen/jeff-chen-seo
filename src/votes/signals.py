from .models import Profile
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Profile)
def index_profile(sender, instance, **kwargs):
    instance.indexing()


