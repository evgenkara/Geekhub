from django.db import models


class Story(models.Model):
    by = models.CharField(max_length=50)
    descendants = models.IntegerField(default=0)
    story_id = models.IntegerField(unique=True)
    score = models.IntegerField(null=True)
    text = models.TextField(null=True, default='')
    time = models.IntegerField(null=True)
    title = models.TextField(null=True)
    type = models.CharField(max_length=50)
    url = models.TextField(null=True, default='')


class Ask(models.Model):
    by = models.CharField(max_length=50)
    descendants = models.IntegerField(blank=True, default=0)
    story_id = models.IntegerField(unique=True)
    score = models.IntegerField(null=True)
    text = models.TextField(null=True, default='')
    time = models.IntegerField(null=True)
    title = models.TextField(null=True)
    type = models.CharField(max_length=50)


class Job(models.Model):
    by = models.CharField(max_length=50)
    story_id = models.IntegerField(null=True, unique=True)
    score = models.IntegerField(null=True)
    text = models.TextField(null=True, default='')
    time = models.IntegerField(null=True)
    title = models.TextField(null=True)
    type = models.CharField(max_length=50)
    url = models.TextField(null=True, default='')
