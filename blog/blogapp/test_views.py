
from django.test import Client
from django.test import TestCase
from faker import Faker
from usersapp.models import BlogUser


class ViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.fake = Faker()
        self.user = BlogUser.objects.create_user(username='test_user', email='test@test.com', password='leo1234567')
        self.user.save()
    def test_statuses(self):
        client = Client()
        #response = client.get('/')# не разобрался
        #self.assertEqual(response.status_code, 200)
        response = client.get('/request')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/send',
                                    {'name': self.fake.name(), 'message': self.fake.text(),
                                     'email': self.fake.email()})
        self.assertEqual(response.status_code, 302)
        '''self.client.login(username='test_user', password='leo1234567')
        response = self.client.get('/users/login/')
        self.assertEqual(response.status_code, 200)'''
    def test_login_required(self):

        response = self.client.get('/users/logout/')
        self.assertEqual(response.status_code, 302)
        #BlogUser.objects.create_user(username='test_user', email='test@test.com', password='leo1234567', is_admin=True)
        '''response = self.client.get('/users/logout/')
        self.assertEqual(response.status_code, 302)'''
        # Он не вошел
        response = self.client.get('/users/login/')
        self.assertEqual(response.status_code, 200)# тут ошибка 302 не разобрался
        # Логиним
        self.client.login(username='test_user', password='leo1234567')
        response = self.client.get('/users/login/')
        self.assertEqual(response.status_code, 200)
    #def test_is_login(self):
        #self.assertEqual(self.user.is_active(), True)











