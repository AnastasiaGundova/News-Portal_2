from .models import Post, Category, Author, User
from rest_framework import serializers


class NewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'type', 'category', 'author', 'title', 'created_at', 'text', 'rating']


class ArticlesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'type', 'category', 'author', 'title', 'created_at', 'text', 'rating']


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', ]


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'user', 'rating']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'user']
