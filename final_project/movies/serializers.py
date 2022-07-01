from rest_framework import serializers
from .models import Category, Movie


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ['name', 'slug', 'category', 'description', 'year', 'trailer']
