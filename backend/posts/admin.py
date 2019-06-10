from django.contrib import admin
from backend.posts.models import Category, Post


admin.site.register(Category)
admin.site.register(Post)