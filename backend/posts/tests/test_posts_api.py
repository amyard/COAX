from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from backend.posts.models import Post, Category
from backend.posts.serializers import PostSerializer, PostDetailSerializer


POST_URL = reverse('posts:post-list')


def detail_url(post_id):
    '''  RETURN POST DETAIL URL   '''
    return reverse('posts:post-detail', args=[post_id])


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

    # DETAIL
    def test_view_post_detail(self):
        '''  viewing the post detail  '''
        post = sample_post(user=self.user)
        post.category.add(sample_category())

        url = detail_url(post.id)
        res = self.client.get(url)

        serializer = PostDetailSerializer(post)

        self.assertEqual(res.data, serializer.data)

    # CREATE
    def test_create_basic_post(self):
        payload = {
            'content': 'AWESOME CONTENT WILL BE HERE',
            'title': 'New title'
        }

        res = self.client.post(POST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        post = Post.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(post, key))

    def create_post_with_category(self):
        '''  create post with category   '''
        cat1 = sample_category(name='Travel')
        cat2 = sample_category(name='Job')
        payload = {
            'title': 'Awesome 1',
            'content': 'blfasfa fadf daf d a',
            'category': [cat1.id, cat2.id]
        }

        res = self.client.post(POST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        post = Post.objects.get(id=res.data['id'])
        categories = post.category.all()

        self.assertEqual(categories.count(), 2)
        self.assertIn(cat1, categories)
        self.assertIn(cat2, categories)
