from django.test import TestCase
from .models import Merchandise, Good, Shop
from usersapp.models import BlogUser
from mixer.backend.django import mixer
# faker - простые данные, например случайное имя
from faker import Faker
fake = Faker()
# Create your tests here.


class MerchandiseTastCaseFacker(TestCase):
    def setUp(self):
        self.user = BlogUser.objects.create_user(username=fake.name(), email='test@test1.com', password='Django123')
    def test_has_file(self):
        self.assertTrue(Good().has_xlsx())
    def test_craete_good(self):
        testGood = Good.objects.create(name='Носки', user=self.user)
        self.assertTrue(testGood.name == 'Носки')
    def test_craete_merch(self):
        user = BlogUser.objects.create_user(username = 'test_user', email = 'test@test.com', password='Django123')
        testShop = Shop.objects.create(name="lenta-super")
        testMerch = Merchandise.objects.create(
            name='Носки', good=fake.name(), imageUrl=fake.name(), priceBefore=0.0,
            priceAfter=0.0, amount=0.0, discount=0.0,
            startDate=fake.date(), endDate=fake.date(), market_name="lenta-super", market=testShop, user=self.user)
        self.assertTrue(testMerch.name == 'Носки')

class MerchandiseTastCaseMixer(TestCase):

    def test_craete_merch(self):

        testMerch = mixer.blend(Merchandise, name = 'Носки')
        print(testMerch.user.username)
        print(testMerch.user.email)
        self.assertTrue(testMerch.name == 'Носки')
    def test_craete_merch1(self):
        testMarket = mixer.blend(Shop, name='Носки')
        testMerch = mixer.blend(Merchandise, name = 'Носки', market__name = 'testMarket')
        print(testMerch.user.username)
        print(testMerch.user.email)
        print(testMerch.market.name)
        self.assertTrue(testMerch.market.name == 'testMarket')


