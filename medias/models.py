from django.db import models

# Create your models here.
class Medias(models.Model):
    TYPE_CHOICES = [
        ("audio", 'audio'),
        ('image', 'image'),
    ]
    file = models.FileField()
    type = models.CharField(null=False, max_length=20, choices=TYPE_CHOICES)

