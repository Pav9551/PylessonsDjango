from django.core.management.base import BaseCommand
from mixer.backend.django import mixer
from blogapp.models import Merchandise
from blogapp.models import  Good, Shop
from usersapp.models import BlogUser


# from blogapp.models import Poll

class Command(BaseCommand):

    def handle(self, *args, **options):
        Good.objects.all().delete()
        Merchandise.objects.all().delete()
        Shop.objects.all().delete()
        BlogUser.objects.filter(is_superuser=False).delete()
        count = 100
        for i in range(count):
            p = (i/count)*100
            print(f'{i}) {p} %')
            mixer.blend(Merchandise)
        print('end')
