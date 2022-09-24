from django.db import models
from civilization.utils.models_utils import *

# Create your models here.
class Civilization(models.Model):
    name = models.CharField(max_length=40)

class Area(models.Model):
    AREA_TYPE_CHOICES = [
        ('C', 'Continent'),
        ('I', 'Island'),
        ('M', 'Mountain'),
        ('S', 'Sea'),
        ('L', 'Lake'),
    ]
    name = models.CharField(max_length=40)
    area_type = models.CharField(max_length=1, default='S')

class Tile(models.Model):
    TILE_TYPE_CHOICES = [
        ('L', 'Land'),
        ('W', 'Water')
    ]
    x = models.IntegerField()
    y = models.IntegerField()
    height = models.FloatField()
    tile_type = models.CharField(max_length=1, default='L', choices=TILE_TYPE_CHOICES)
    owner = models.ForeignKey(Civilization, blank=True, null=True, related_name="tiles", on_delete=models.CASCADE)
    areas = models.ManyToManyField(Area, related_name="tiles")

    class Meta:
        unique_together = ('x', 'y')

    @property
    def height_m(self):
        if self.tile_type == "L": return f"{self.height*5000:.2f}"
        else: return f"{self.height*1000:.2f}"

    @property
    def color(self):
        if self.tile_type == 'L':
            return get_land_color(self.height)
        else:
            return get_water_color(self.height)

    def is_area_type(self, area_type):
        if self.areas.filter(area_type=area_type):
            return True
        return False

    # left, right, top, bottom
    def is_adjacent_to_tile_type(self, tile_type):
        x, y = self.x, self.y
        coords = [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]
        is_adjacent = []
        for x, y in coords:
            try:
                tile = Tile.objects.get(x=x, y=y)
                if tile.tile_type == tile_type:
                    is_adjacent.append(True)
                else:
                    is_adjacent.append(False)
            except:
                is_adjacent.append(True)
        return is_adjacent

    def get_border_style(self):
        border_style = ""
        if self.tile_type == 'L':
            return border_style
        else:
            adjacent_dict = {
                0: 'left',
                1: 'right',
                2: 'top',
                3: 'bottom',
            }
            is_adjacent = self.is_adjacent_to_tile_type('L')
            for i, adjacent_bool in enumerate(is_adjacent):
                if adjacent_bool:
                    border_style += f"border-{adjacent_dict[i]}: 3px solid #DADF47; "
            return border_style

    def __str__(self) -> str:
        return f"({self.x}, {self.y}), type {self.tile_type}, {self.height_m}m, color {self.color}"