from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from backend.posts.models import Post, Category
from backend.posts.serializers import PostSerializer


POST_URL = reverse('posts:post-list')



def sample_category(name='Home'):
    return Category.objects.create(name=name)


def sample_post(user, **params):
    defaults = {
        'title': 'New title for post',
        'content': 'Bla bli blo'
    }
    defaults.update(**params)
    return Post.objects.create(author=user, **defaults)



class PublicPostApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(POST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePostApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user('test@gmail.con', 'zaza1234')
        self.client.force_authenticate(self.user)

    def test_retrieve_posts(self):
        '''   retrieving list of posts  '''
        sample_post(user=self.user)
        sample_post(user=self.user)

        res = self.client.get(POST_URL)

        posts = Post.objects.all().order_by('-id')
        serializer = PostSerializer(posts, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_posts_limited_to_user(self):
        '''   retrieving posts of specific user '''
        user2 = get_user_model().objects.create_user('bla@gmail.com', 'pass' )

        sample_post(user=self.user)
        sample_post(user=user2)

        res = self.client.get(POST_URL)

        posts = Post.objects.filter(author=user2)
        serializer = PostSerializer(posts, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)