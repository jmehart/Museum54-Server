from django.db import models
from .artist import Artist
from .classification import Classification
from .style import Style
from .genre import Genre
from .medium import Medium

class Art(models.Model):
    title = models.CharField(max_length=60)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="art", default=None)
    description = models.TextField(null=True)
    dateMade = models.CharField(max_length=30)
    dateAcquired = models.CharField(max_length=30)
    dateEntered = models.DateTimeField(auto_now_add=True)
    curator = models.ForeignKey("curator", on_delete=models.CASCADE)
    location = models.CharField(max_length=30)
    dimensions = models.CharField(max_length=60)
    classification = models.ManyToManyField(Classification, related_name="artclassification")
    style = models.ManyToManyField(Style, related_name="styles", default=None)
    genre = models.ManyToManyField(Genre, related_name="genres", default=None)
    medium = models.ManyToManyField(Medium, related_name="mediums", default=None)
    framed = models.BooleanField(default=False)
    signature = models.BooleanField(default=False)
    image = models.ImageField(
        upload_to='media', default="")