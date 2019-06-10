from django.contrib import admin
from backend.posts.models import Category, Post, IpAccess


admin.site.register(Category)
admin.site.register(Post)
admin.site.register(IpAccess)