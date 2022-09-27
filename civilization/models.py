from django.db import models
from civilization.utils.models_utils import *

# Create your models here.
class Resource(models.Model):
    class Meta:
        ordering = ['food', 'production', 'culture']
    name = models.CharField(max_length=20)
    food = models.IntegerField()
    production = models.IntegerField()
    culture = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.name} +{self.food} Food, +{self.production} Production, +{self.culture} Culture"

class Civilization(models.Model):
    name = models.CharField(max_length=40)

class Area(models.Model):
    class Meta:
        ordering = ['area_type', 'name']

    AREA_TYPE_CHOICES = [
        ('C', 'Continent'),
        ('I', 'Island'),
        ('M', 'Mountain'),
        ('S', 'Sea'),
        ('L', 'Lake'),
        ('R', 'River'),
    ]
    name = models.CharField(max_length=40)
    area_type = models.CharField(max_length=1, default='S', choices=AREA_TYPE_CHOICES)

    def __str__(self) -> str:
        return f"{self.get_area_type_display()} {self.name}"

class Tile(models.Model):
    TILE_TYPE_CHOICES = [
        ('L', 'Land'),
        ('W', 'Water')
    ]
    x = models.IntegerField()
    y = models.IntegerField()
    height = models.FloatField()
    tile_type = models.CharField(max_length=1, default='L', choices=TILE_TYPE_CHOICES)
    owner = models.ForeignKey(Civilization, blank=True, null=True, related_name="tiles", on_delete=models.SET_NULL)
    resource = models.ForeignKey(Resource, blank=True, null=True, related_name="tiles", on_delete=models.SET_NULL)
    areas = models.ManyToManyField(Area, related_name="tiles")

    class Meta:
        unique_together = ('x', 'y')

    @property
    def height_m(self):
        if self.tile_type == "L": return f"{self.height*5000:.2f}"
        else: return f"{self.height*1000:.2f}"

    @property
    def color(self):
        if self.resource: return "000"
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

    # left, right, top, bottom
    def is_adjacent_to_area_type(self, area_type):
        x, y = self.x, self.y
        coords = [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]
        is_adjacent = []
        for x, y in coords:
            try:
                tile = Tile.objects.get(x=x, y=y)
                if tile.areas.filter(area_type=area_type):
                    is_adjacent.append(True)
                else:
                    is_adjacent.append(False)
            except:
                is_adjacent.append(True)
        return is_adjacent

    # Border style for rivers
    def get_border_style(self):
        border_style = ""
        if self.is_area_type('R'):
            adjacent_dict = {
                0: 'left',
                1: 'right',
                2: 'top',
                3: 'bottom',
            }
            is_adjacent = self.is_adjacent_to_tile_type('L')
            for i, adjacent_bool in enumerate(is_adjacent):
                if adjacent_bool:
                    border_style += f"border-{adjacent_dict[i]}: 2px solid #{get_land_color(self.height)}; "
        return border_style

    def get_title_description(self):
        description = f"({ self.x }, { self.y }) { self.tile_type } &#010; { self.height_m }m "
        if self.resource:
            description += f" &#010; {self.resource.name}"
        for area in self.areas.all():
            description += f" &#010; {area.name} ({area.get_area_type_display()})"
        return description

    def __str__(self) -> str:
        return f"({self.x}, {self.y}), type {self.tile_type}, {self.height_m}m, color {self.color}"