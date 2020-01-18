from django.db import models

# Create your models here.
from django.conf import settings


class Profile(models.Model):
    nickname = models.CharField(max_length=10)
    exp = models.IntegerField(default=0)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
