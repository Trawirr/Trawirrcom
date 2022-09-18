from django.db import models
import requests

class BorsukUlamPoint(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    city = models.CharField(max_length=50)
    distance = models.FloatField()
    direction = models.CharField(max_length=2, default="")
    temperature = models.FloatField()

    def __str__(self) -> str:
        return f"({self.lat}, {self.lon}) - {self.distance}km {self.direction} from {self.city}, temperature {self.temperature}'C"

    @property
    def coords(self):
        if self.lat > 0:
            lat = f"{self.lat:.3f}°N"
        else:
            lat = f"{abs(self.lat):.3f}°S"
        if self.lon > 0:
            lon = f"{self.lon:.3f}°E"
        else:
            lon = f"{abs(self.lon):.3f}°W"
        return f"({lat}, {lon})"

    @property
    def temperature_2f(self):
        return f"{self.temperature:.2f}°C"

    def get_map_link(self):
        return f"https://www.google.com/maps/place/{self.lat}+{self.lon}"

    def get_city_link(self):
        return f"https://en.wikipedia.org/wiki/{self.city.split(',')[0]}"

    def city_exists(self):
        r = requests.get(self.get_city_link())
        if r.status_code != 200:
            return False
        return True