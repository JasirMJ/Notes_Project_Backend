from django.db import models

# Create your models here.

class Notes(models.Model):
    heading = models.CharField(max_length=120,null=False)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    note_background_color = models.CharField(default="#FFFFFF",max_length=120,null=True)