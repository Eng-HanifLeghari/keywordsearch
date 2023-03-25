from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Blog(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    image_field = models.ImageField(upload_to='media/')
    description = models.TextField()

    def __str__(self):
        return self.name