from django.db import models

class Medium(models.Model):
    type = models.CharField(max_length=60)