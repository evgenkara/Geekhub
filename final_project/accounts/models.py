from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='no_image.png', upload_to='profile_images')
    info = models.TextField(blank=True)
    watchlist = models.ManyToManyField(Movie, related_name='movies', blank=True)
    google_auth = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return self.user.username
