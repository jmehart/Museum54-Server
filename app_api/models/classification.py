from django.db import models

class Classification(models.Model):
    type = models.CharField(max_length=60)