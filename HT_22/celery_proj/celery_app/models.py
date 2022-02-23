from django.db import models


class Story(models.Model):
    by = models.CharField(max_length=50)
    story_id = models.IntegerField(unique=True, default=0)
    score = models.IntegerField(null=True)
    text = models.TextField(null=True, default='')
    time = models.IntegerField(null=True)
    title = models.TextField(null=True)
    type = models.CharField(max_length=50)

    class Meta:
        abstract = True


class Show(Story):
    descendants = models.IntegerField(default=0)
    url = models.TextField(null=True, default='')

    class Meta:
        db_table = 'showstories'


class New(Story):
    descendants = models.IntegerField(default=0)
    url = models.TextField(null=True, default='')

    class Meta:
        db_table = 'newstories'


class Ask(Story):
    descendants = models.IntegerField(blank=True, default=0)

    class Meta:
        db_table = 'askstories'


class Job(Story):
    url = models.TextField(null=True, default='')

    class Meta:
        db_table = 'jobstories'
