from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


class Contact(models.Model):
    User = get_user_model()
    #user that requested the relationship
    user_from = models.ForeignKey(User, related_name='rel_from_set', on_delete=models.CASCADE)
    #user that the request was sent to
    user_to = models.ForeignKey(User, related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
        ]
        ordering = ['-created']

    def __str__(self):
        return f' {self.user_from} follows {self.user_to}' 