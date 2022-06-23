from django.db import models

class Artist(models.Model):
    name = models.CharField(max_length=60)
    birth = models.CharField(max_length=30)
    death = models.CharField(blank=True, max_length=30)
    bio = models.TextField(null=True)
    nationality = models.CharField(max_length=30)
    dateEntered = models.DateTimeField(auto_now_add=True)
    curator = models.ForeignKey("curator", on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='media', default="")