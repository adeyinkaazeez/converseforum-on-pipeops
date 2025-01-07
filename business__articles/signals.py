from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Business_Articles

@receiver(m2m_changed, sender=Business_Articles.likes.through)
def likes_changed(sender, instance, **kwargs):
    instance.total_likes = instance.likes.count()
    instance.save()