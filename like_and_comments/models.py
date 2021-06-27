from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from posts.models import Posts

class Comments(models.Model):
    posts = models.ForeignKey(Posts,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.TextField(null=False)

class Likes(models.Model):
    posts = models.ForeignKey(Posts,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    like = models.IntegerField(default=0)