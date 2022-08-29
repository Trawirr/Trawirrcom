from distutils.command.upload import upload
from django.conf import settings
from django.db import models
from datetime import datetime, date

class Author(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20, default="")
    date = models.DateField(default=date.today)
    profile_image = models.ImageField(upload_to='static/upload/profile_images/')

    def __str__(self) -> str:
        return f"{self.nickname}, created on {self.date}"

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=50, default="Title")
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    text = models.TextField()
    image = models.ImageField(upload_to='static/upload/article_images/')

    def __str__(self) -> str:
        return f"by {self.author.nickname}, created on {self.date}, text: {self.text[:20]}..."