from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Happenings

@receiver(m2m_changed, sender=Happenings.likes.through)
def likes_changed(sender, instance, **kwargs):
    instance.total_likes = instance.likes.count()
    instance.save()