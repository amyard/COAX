from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status




CREATE_USER_URL = reverse('user:create')
TOKEN_URL=reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)



class PublicUserApiTests(TestCase):
    ''' Test the users API (public) '''
    def setUp(self):
        self.client = APIClient()


    def test_create_valid_user_success(self):
        ''' creating user with valid info - success '''
        payload = {
            'email': 'test@gmail.com',
            'password': 'zaza1234',
            'name': 'Test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)


    def test_user_exists(self):
        ''' such user is already exists '''
        payload = { 'email':'test@gmail.com', 'password':'password'}
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        ''' password is too short '''
        payload = {'email': 'test@gmail.com', 'password': 'pwd'}
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exists)


    def test_create_token_for_user(self):
        ''' creating token for user '''
        payload = {'email':'test@gmail.com', 'password':'zaza1234'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_Create_token_invalid_credentials(self):
        ''' token is not created if invalid data '''
        create_user(email='test@gmail.com', password='zaza1234')
        payload = {'email': 'test@gmail.com', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        ''' token not created is user does not exists '''
        payload = {'email': 'test@gmail.com', 'password': 'zaza1234'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        ''' test that email and password required '''
        res = self.client.post(TOKEN_URL, {})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_retrieve_user_unauthorized(self):
        ''' authentication is required for users '''
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)



class PrivateUserApiTests(TestCase):
    '''  test API that require authentication  '''

    def setUp(self):
        self.user = create_user(email='test@gmail.com', password='zaza1234', name='TEST')
        self.client = APIClient()
        self.client.force_authenticate(user = self.user)

    def test_retrieve_profile_success(self):
        '''   test retriving profile for logged user  '''
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {'name':self.user.name, 'email':self.user.email})

    def test_post_me_not_allowed(self):
        '''  POST is not allowed on the me url  '''
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        '''  updating the user profile for authenticated users  '''
        payload = {'name': 'New name', 'password':'newpassword'}
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()

        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)