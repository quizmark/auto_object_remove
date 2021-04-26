from django.db import models

class Post(models.Model):
    objects=models.Manager()
    rating = models.FloatField(null=True)
# Create your models here.
