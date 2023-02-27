
from django.test import Client
from django.test import TestCase
from faker import Faker
from usersapp.models import BlogUser


class ViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.fake = Faker()

    def test_statuses(self):
        client = Client()
        response = client.get('/request')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/send',
                                    {'name': self.fake.name(), 'message': self.fake.text(),
                                     'email': self.fake.email()})
        self.assertEqual(response.status_code, 302)
        self.client.login(username='test_user', password='leo1234567')
        response = self.client.get('/users/login')
        self.assertEqual(response.status_code, 301)





