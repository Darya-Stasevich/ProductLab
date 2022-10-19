from rest_framework import serializers

from api.models import File, Article


class FileSerializer(serializers.ModelSerializer):
    """Сериализатор для модели File"""
    class Meta:
        model = File
        fields = ['file', ]


class ArticleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Article"""
    class Meta:
        model = Article
        fields = ['article', ]