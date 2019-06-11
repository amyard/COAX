from django.test import TestCase
from django.contrib.auth import get_user_model

from backend.posts import models


def sample_user(email='test@gmail.com', password = 'zaza1234'):
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    def test_category_str(self):
        '''  categories string representation  '''
        categories = models.Category.objects.create(name='Travel')

        self.assertEqual(str(categories), categories.name)

    def test_post_str(self):
        '''  Test the posts string representation  '''
        post = models.Post.objects.create(
            author=sample_user(),
            title='First Post',
            content='Here will be new content'
        )
        self.assertEqual(str(post), post.title)

    def test_ip_access_str(self):
        '''  ip access string representation  '''
        ip = models.IpAccess.objects.create(ip='192.168.0.1')

        self.assertEqual(str(ip), ip.ip)