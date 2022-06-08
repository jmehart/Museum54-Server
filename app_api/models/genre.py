from django.db import models

class Genre(models.Model):
    type = models.CharField(max_length=60)