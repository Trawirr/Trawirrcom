from re import T
from django.db import models

# Create your models here.
class Civilization(models.Model):
    name = models.CharField(max_length=40)

class Area(models.Model):
    name = models.CharField(max_length=40)

class Tile(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    height = models.IntegerField()
    owner = models.ForeignKey(Civilization, blank=True, null=True, related_name="tiles", on_delete=models.CASCADE)
    areas = models.ManyToManyField(Area, related_name="tiles")

    class Meta:
        unique_together = ('x', 'y')