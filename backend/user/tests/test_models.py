from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successfull(self):
        ''' Create an user with email successfull '''

        email='test@gmail.com'
        password='12121212'

        user = get_user_model().objects.create_user(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))


    def test_new_user_email_normalized(self):
        ''' test the email for a new user is normalized '''
        email='test@GMAIL.COM'
        user=get_user_model().objects.create_user(email, '12121212')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        ''' creating user with no email raises error '''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, '12121212')

    def test_create_new_superuser(self):
        ''' Creating new superuser '''

        user = get_user_model().objects.create_superuser('test@gmail.com', 'zaza1234')

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)