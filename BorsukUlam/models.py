from django.db import models

# Create your models here.
class BorsukUlamPoint(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    city = models.CharField(max_length=50)
    distance = models.FloatField()
    temperature = models.FloatField()

    def __str__(self) -> str:
        return f"({self.lat}, {self.lon}) - {self.distance}km from {self.city}, temperature {self.temperature}'C"