from django.db import models


class File(models.Model):
    """Модель для файла"""
    file = models.FileField(upload_to='files')


class Article(models.Model):
    """Модель для артикула"""
    article = models.IntegerField()
