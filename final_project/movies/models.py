from django.urls import reverse
from django.db import models
from embed_video.fields import EmbedVideoField
from django.contrib.auth.models import User

from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating


User._meta.get_field('email')._unique = True


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('movies:movie_list_by_category',
                       args=[self.slug])


class Movie(models.Model):
    category = models.ManyToManyField(Category, related_name='movies')
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(default='no_image.png', upload_to='movies/', blank=True)
    description = models.TextField(blank=True)
    year = models.IntegerField(blank=True)
    trailer = EmbedVideoField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    ratings = GenericRelation(Rating, related_query_name='movies')

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('movies:movie_detail',
                       args=[self.id, self.slug])


class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"{self.movie.name} comment by {self.name}"
