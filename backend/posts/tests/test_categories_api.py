from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from backend.posts.models import Category
from backend.posts.serializers import CategorySerializer



CATEGORY_URL = reverse('posts:category-list')


class PublicCategoryApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()


    def test_login_is_required(self):
        res = self.client.get(CATEGORY_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCategoryApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user('test@gmail.com', 'zaza1234')
        self.client.force_authenticate(self.user)

    def test_retrieve_category_list(self):
        '''  retrive list of categories  '''
        Category.objects.create(name='Travel')
        Category.objects.create(name='Study')

        res = self.client.get(CATEGORY_URL)
        category = Category.objects.all().order_by('-name')
        serializer = CategorySerializer(category, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_category_success(self):
        '''  create new category  '''
        payload = {'name': 'Job'}
        self.client.post(CATEGORY_URL, payload)

        exists = Category.objects.filter(name=payload['name']).exists()
        self.assertTrue(exists)

    def test_create_category_invalid(self):
        payload = {'name': ''}
        res = self.client.post(CATEGORY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)