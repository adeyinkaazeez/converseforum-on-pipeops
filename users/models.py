from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from PIL import Image
from django.utils import timezone
from django.urls import reverse


# Create your models here.

class CustomUser(AbstractUser):
    STATUS = (
        ('regular', 'regular'),
        ('subscriber', 'subscriber'),
        ('moderator', 'moderator'),
    )

    email = models.EmailField(unique=True)
    status = models.CharField(max_length=100, choices=STATUS, default='regular')
    description = models.TextField("Description", max_length=600, default='', blank=True)
    following = models.ManyToManyField('self', through='Contact', related_name="followers", symmetrical=False)
    def get_absolute_url(self):
        return reverse('post_author',
                       args=[self.id])
    

User = get_user_model()
class Contact(models.Model):
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

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
   
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',
                                                          default='avatar.png',)
    about = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=100, null=True)
    #following = models.ManyToManyField(CustomUser, through=Contact, related_name="followers", symmetrical=False)
    def __str__(self):
        return f'Profile of {self.user.username}'
    
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.photo.path)

        if img.height >300 or img.width > 350:
            output_size = (350,300)
            img.thumbnail(output_size)
            img.save(self.photo.path)

class SubscribedUsers(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=100)
    created_date = models.DateTimeField('Date created', default = timezone.now)

    def __str__(self):
        return self.email

