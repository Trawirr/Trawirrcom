from distutils.command.upload import upload
from django.conf import settings
from django.db import models
from datetime import datetime, date

class Variable(models.Model):
    name = models.CharField(max_length=20)
    value = models.CharField(max_length=20)

class Tag(models.Model):
    name = models.CharField(max_length=20, primary_key=True)

class Author(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20, default="")
    date = models.DateField(default=date.today)
    profile_image = models.ImageField(upload_to='static/upload/profile_images/')

    def __str__(self) -> str:
        return f"{self.nickname}, created on {self.date}"

# Create your models here.
class Article(models.Model):
    class Meta:
        ordering = ['-date']
    
    title = models.CharField(max_length=50, default="Title")
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.today())
    text = models.TextField()
    image = models.ImageField(upload_to='static/upload/article_images/')
    tags = models.ManyToManyField(Tag)

    def __str__(self) -> str:
        return f"by {self.author.nickname}, created on {self.date}, text: {self.text[:20]}..."

    @property
    def date_dmy(self):
        return self.date.strftime("%d %b %Y")

    @property
    def thumbnail_text(self):
        words = self.text.split(' ')
        for i in range(len(words)):
            if len(' '.join(words[:i])) > 100 - 2 * len(self.title):
                return ' '.join(words[:i-1])
        return self.text

    @property
    def parsed_text(self):
        return '\n'.join([f"<p>{t}</p>" for t in self.text.split('\n')])