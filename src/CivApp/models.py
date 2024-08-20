from django.db import models

class Map(models.Model):
    name = models.CharField(max_length=20, default="default_map_name")
    seed = models.IntegerField(default=1998)
    size = models.IntegerField(default=100)
    octaves = models.CharField(max_length=20, default="3 6 12 24")
    sea_level = models.FloatField(default=0.5)

    # TO BE ADDED - map categories like 'archipelago', 'pangea' 'islands' 'two continents' etc.

class Area(models.Model):
    TYPE_CHOICES = (
        ("W", "water"),
        ("L", "land")
    )
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    x = models.IntegerField()
    y = models.IntegerField()
    category = models.CharField(max_length=1, choices=TYPE_CHOICES, default="l")

