from django.db import models
from django.db.models import TextField, CharField, URLField, IntegerField


class WebsiteType(models.Model):
    name = CharField(max_length=400)


class Site(models.Model):
    name = CharField(max_length=500)
    url = URLField(max_length=1000)
    type = models.ForeignKey(WebsiteType, default=None, blank=True)


class SocialSearch(models.Model):
    search = CharField(max_length=1000, unique=True)
    picture_url = URLField(blank=True)
    number = IntegerField(default=0)

    class Meta:
        ordering = ['-number']
