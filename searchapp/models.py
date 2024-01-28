from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Article(models.Model):
    article_name = models.CharField(max_length=250)
    article_link = models.CharField(max_length=250)
    article_date = models.DateTimeField()

    def __str__(self):
        return self.article_name
