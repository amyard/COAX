from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from backend.posts.models import Category, Post

from backend.posts import serializers


class CategoryViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        return self.queryset.order_by('-name')

    def perform_create(self, serializer):
        serializer.save()


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PostSerializer
    queryset = Post.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(author = self.request.user).order_by('-id')

    def get_serializer_class(self):
        '''  return needed serializer class  '''
        if self.action == 'retrieve':
            return serializers.PostDetailSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)