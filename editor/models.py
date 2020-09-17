from django.db import models


class Sound(models.Model):
    name = models.CharField(max_length=80)
    filename = models.CharField(max_length=80)


