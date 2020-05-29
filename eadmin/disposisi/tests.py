from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password

from .models import MemoSimple


class MemoSimpleModelTests(TestCase):

    def test_create_model(self):
        """
        """
        memosimple_subject1 = MemoSimple.objects.create(subject="Subject 1", information="Information 1",
                                                        sender="Sender 1")
        self.assertIs(memosimple_subject1.subject, "Subject 1")

    def test_default_state_for_created_module(self):
        """
        """
        memosimple_subject1 = MemoSimple.objects.create(subject="Subject 1", information="Information 1",
                                                        sender="Sender 1")
        self.assertIs(memosimple_subject1.state, 0)


class MemoSimpleAPITests(APITestCase):
    def setUp(self):
        """
        Setup user for testing
        """
        pwd = make_password('password_01')
        user = User.objects.create(username='username_01', password=pwd)
        user.save()
        """
        Obtain JWT token for endpoint requiring auth
        """
        url = reverse("token_obtain_pair")
        response = self.client.post(url, {'username': 'username_01', 'password': 'password_01'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.token = response.data['access']

    def test_create_memosimple_unauthenticated(self):
        """
        Ensure we can create a new memosimple object but unauthenticated.
        """
        url = reverse("disposisi:memosimple-api-list-create")
        data = {
            "subject": "Subject 1",
            "information": "Information 1",
            "sender": "Sender 1"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_and_get_jwt_token(self):
        """
        Ensure login process is working and tokens is retrieved
        :return:
        """
        url = reverse("token_obtain_pair")
        response = self.client.post(url, {'username': 'username_01', 'password': 'password_01'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        token = response.data['access']

    def test_create_memosimple_authenticated(self):
        """
        Ensure we can create a new memosimple object but authenticated.
        """
        url = reverse("disposisi:memosimple-api-list-create")
        data = {
            "subject": "Subject 1",
            "information": "Information 1",
            "sender": "Sender 1"
        }

        # self.assertTrue(self.client.login(username='username_01', password='password_01'))
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MemoSimple.objects.count(), 1)
        self.assertEqual(MemoSimple.objects.get().subject, 'Subject 1')
