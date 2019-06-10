from django.db import models
from django.conf import settings
from django.utils import timezone



class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    title = models.CharField(max_length = 255)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    category = models.ManyToManyField('Category')

    def __str__(self):
        return self.title