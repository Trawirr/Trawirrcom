from django.db import models

class Card(models.Model):
    name = models.CharField(max_length=30)
    jpg = models.ImageField(upload_to='images/')
    gif = models.ImageField(upload_to='images/')