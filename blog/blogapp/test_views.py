
from django.test import Client
from django.test import TestCase
from faker import Faker
from usersapp.models import BlogUser


class ViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.fake = Faker()

    def test_statuses(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Что мы можем проверить
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)