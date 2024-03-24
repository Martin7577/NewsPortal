from .models import *
from rest_framework import serializers


class PostSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Post
       fields = ['id', 'header', ]


class CommentSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Comment
       fields = ['id', 'text_comment', ]


class CategorySerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Category
       fields = ['id', 'nameCategory', ]