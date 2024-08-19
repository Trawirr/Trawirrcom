from django.db import models

class Map(models.Model):
    name = models.CharField(max_length=20, default="default_map_name")

class Area(models.Model):
    TYPE_CHOICES = (
        ("W", "water"),
        ("L", "land")
    )
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    x = models.IntegerField()
    y = models.IntegerField()
    area_type = models.CharField(max_length=1, choices=TYPE_CHOICES, default="l")

