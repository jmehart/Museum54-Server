from django.db import models
from .artist import Artist
from .classification import Classification
from .style import Style
from .genre import Genre
from .medium import Medium

class Art(models.Model):
    title = models.CharField(max_length=60)
    artistId = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="artists", default=None)
    description = models.TextField(null=True)
    dateMade = models.CharField(max_length=30)
    dateAcquired = models.CharField(max_length=30)
    dateEntered = models.DateTimeField(auto_now_add=True)
    curator = models.ForeignKey("curator", on_delete=models.CASCADE)
    location = models.CharField(max_length=30)
    dimensions = models.CharField(max_length=60)
    classificationId = models.ManyToManyField(Classification, on_delete=models.CASCADE, related_name="classification", default=None)
    styleId = models.ManyToManyField(Style, on_delete=models.CASCADE, related_name="styles", default=None)
    genreId = models.ManyToManyField(Genre, on_delete=models.CASCADE, related_name="genres", default=None)
    mediumId = models.ManyToManyField(Medium, on_delete=models.CASCADE, related_name="mediums", default=None)
    framed = models.BooleanField(Default=False)
    signature = models.BooleanField(Default=False)
    image = models.URLField()