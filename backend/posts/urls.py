from django.urls import path, include
from rest_framework.routers import DefaultRouter

from backend.posts import views

router = DefaultRouter()

router.register('categories', views.CategoryViewSet)


app_name = 'posts'


urlpatterns = [
    path('', include(router.urls))
]