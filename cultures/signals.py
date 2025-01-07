from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Cultures

@receiver(m2m_changed, sender=Cultures.likes.through)
def likes_changed(sender, instance, **kwargs):
    instance.total_likes = instance.likes.count()
    instance.save()