from rest_framework import serializers

from backend.posts.models import Category, Post


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']
        read_only_fields = ('id',)


class PostSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all())

    class Meta:
        model = Post
        fields = ('id', 'title', 'date_posted', 'content', 'category')
        read_only_fields = ('id',)


class PostDetailSerializer(PostSerializer):
    category = CategorySerializer(many=True, read_only=True)