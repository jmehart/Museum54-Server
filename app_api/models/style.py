from django.db import models

class Style(models.Model):
    type = models.CharField(max_length=60)