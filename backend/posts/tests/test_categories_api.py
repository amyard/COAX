from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from backend.posts.models import Category
from backend.posts.serializers import CategorySerializer



CATEGORY_URL = reverse('posts:category-list')

from backend.posts.models import IpAccess
from django.test.client import Client as HttpClient


# WORKED WITH TOKEN AUTHENTICATION
# class PublicCategoryApiTest(TestCase):
#     def setUp(self):
#         IpAccess.objects.create(ip='168.255.2.48')
#         self.client = HttpClient(REMOTE_ADDR='168.255.2.48')
#
#
#
#     def test_login_is_not_required(self):
#         res = self.client.get(CATEGORY_URL)
#         # self.assertEqual(res.status_code, status.HTTP_200_OK)
#         print(res)



# class PrivateCategoryApiTest(TestCase):
#
#     def setUp(self):
#         self.client = APIClient()

    # def test_retrieve_category_list_has_access(self):
    #     '''  retrive list of categories  '''
    #     Category.objects.create(name='Travel')
    #     Category.objects.create(name='Study')
    #     IpAccess.objects.create(ip='127.0.0.1')
    #
    #     res = self.client.get(CATEGORY_URL, REMOTE_ADDR="127.0.0.1")
    #     category = Category.objects.all().order_by('-name')
    #     serializer = CategorySerializer(category, many=True)
    #
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data, serializer.data)

    # def test_create_category_success(self):
    #     '''  create new category  '''
    #     payload = {'name': 'Job'}
    #     self.client.post(CATEGORY_URL, payload)
    #
    #     exists = Category.objects.filter(name=payload['name']).exists()
    #     self.assertTrue(exists)
    #
    # def test_create_category_invalid(self):
    #     payload = {'name': ''}
    #     res = self.client.post(CATEGORY_URL, payload)
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)