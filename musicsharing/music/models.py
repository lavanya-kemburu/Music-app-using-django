from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)

class MusicFile(models.Model):
    PUBLIC = 'public'
    PRIVATE = 'private'
    PROTECTED = 'protected'
    PRIVACY_CHOICES = [
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
        (PROTECTED, 'Protected'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='music/')
    privacy = models.CharField(
        max_length=10,
        choices=PRIVACY_CHOICES,
        default=PUBLIC,
    )

class Access(models.Model):
    music_file = models.ForeignKey(MusicFile, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

