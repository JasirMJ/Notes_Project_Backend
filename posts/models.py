from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from medias.models import Medias


class Posts(models.Model):
    title = models.CharField(max_length=120,null=True)
    files = models.ManyToManyField(Medias)
    desc = models.TextField(null=True)
    posted = models.ForeignKey(User,on_delete=models.CASCADE)
    weight = models.IntegerField(default=1000)