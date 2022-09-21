from django.db import models
from civilization.utils.models_utils import *

# Create your models here.
class Civilization(models.Model):
    name = models.CharField(max_length=40)

class Area(models.Model):
    name = models.CharField(max_length=40)

class Tile(models.Model):
    TILE_TYPE_CHOICES = [
        ('L', 'Land'),
        ('W', 'Water')
    ]
    x = models.IntegerField()
    y = models.IntegerField()
    height = models.FloatField()
    tile_type = models.CharField(max_length=1, default='L')
    owner = models.ForeignKey(Civilization, blank=True, null=True, related_name="tiles", on_delete=models.CASCADE)
    areas = models.ManyToManyField(Area, related_name="tiles")

    class Meta:
        unique_together = ('x', 'y')

    @property
    def height_m(self):
        return f"{self.height*5000:.2f}"

    @property
    def color(self):
        if self.tile_type == 'L':
            return get_land_color(self.height)
        else:
            return get_water_color(self.height)

    def __str__(self) -> str:
        return f"({self.x}, {self.y}), type {self.tile_type}, {self.height_m}m, color {self.color}"