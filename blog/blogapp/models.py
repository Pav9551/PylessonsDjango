from django.db import models
from usersapp.models import BlogUser
from edadeal_new import ED
import re
import pandas as pd
import os
from pathlib import Path
from django.utils.functional import cached_property
from django.forms import HiddenInput
# Create your models here.

class Category(models.Model):
    #Id не надо, он уже сам появиться
    name = models.CharField(max_length= 16, unique=True)
    description = models.TextField(blank= True)
    '''
    # Основные типы полей
    # data
    models.DateField
    models.DateTimeField
    models.TimeField
    # число
    models.IntegerField
    models.PositiveIntegerField
    models.PositiveSmallIntegerField
    models.FloatField
    models.DecimalField
    # логический
    models.BooleanField
    # Байты
    models.BinaryField
    # Картинка
    models.ImageField
    # Файл
    models.FileField
    # Url, email
    models.URLField
    models.EmailField
    '''
    def __str__(self):
        return self.name
class Tag(models.Model):
    name = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.name
class ActiveManager(models.Manager):
    def get_queryset_user(self, username=None):
        queryset = super().get_queryset()
        if username:
            list_of_Merch = Merchandise.objects.filter(user = username).values_list('good').distinct()
            list_result = [entry[0] for entry in list_of_Merch]  # converts QuerySet into Python list
            query = Good.objects.filter(user=username)
            query.update(good_count=0)
            query = Good.objects.filter(name__in=list_result, user = username)
            query.update(good_count = 1)
            queryset = queryset.filter(user = username)
        return queryset
    def get_queryset_max_discount(self):
        queryset = super().get_queryset()
        return queryset

class IsActiveMixin(models.Model):
    objects = models.Manager()
    active_objects = ActiveManager()
    class Meta:
        abstract = True
class Post(models.Model):
    name = models.CharField(max_length= 32, unique= True)
    text = models.TextField()
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now= True)
    # Связь с категорией
    # один ко многим
    category = models.ForeignKey(Category, on_delete= models.CASCADE)
    # Связь с тегами
    # многим ко многим
    tags = models.ManyToManyField(Tag)
    def __str__(self):
        return self.name
class Post_for_Coincidence(models.Model):
    name = models.CharField(max_length= 32, unique= False)
    text = models.TextField()
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now= True)
    user = models.ForeignKey(BlogUser, on_delete=models.CASCADE)

    def __str__(self):
        #return self.name
        return (f'{self.name}')

class TimeStamp(models.Model):
    """
    Abstract - для нее не создаются новые таблицы
    данные хранятся в каждом наследнике
    """
    startDate = models.DateTimeField(auto_now_add=True)
    endDate = models.DateTimeField(auto_now= True)
    class Meta:
        abstract = True

class Good(models.Model):
    objects = models.Manager()
    active_objects = ActiveManager()
    name = models.CharField(max_length=32, unique=False)
    user = models.ForeignKey(BlogUser, on_delete=models.CASCADE)
    good_count = models.IntegerField(default=0)
    #user = models.ManyToManyField(BlogUser)
    def __str__(self):
        #return self.name
        return (f'{self.name}')
    def has_xlsx(self):
        # Build paths inside the project like this: BASE_DIR / 'subdir'.
        BASE_DIR = Path(__file__).resolve().parent.parent
        xlx_file = BASE_DIR / 'goods.xlsx'
        return os.path.isfile(xlx_file)
    #def validate_unique(self, exclude=None):
    def is_unique(self, name = 'Носки', user = 'user'):
        print(f'функция.{name}.{user}')
        user = BlogUser.objects.filter(username=user)
        coinc, created = Coincidence.objects.get_or_create(name = name)
        coinc.users.add(user[0])
        query = Good.objects.filter(name=name, user = user[0]).exists()
        if query == True:
            #print(f'Уже существует')
            return False
        else:
            #print(f'Еще не было')
            return True
    def del_good(self, name = 'Носки', user = 'user'):
        print(f'функция.{name}.{user}')
        user = BlogUser.objects.filter(username=user)
        coinc, created = Coincidence.objects.get_or_create(name = name)
        coinc.users.remove(user[0])
        query = Good.objects.filter(name=name, user = user[0]).exists()
        if query == True:
            #print(f'Уже существует')
            return False
        else:
            #print(f'Еще не было')
            return True
class Coincidence(models.Model):
    users = models.ManyToManyField(BlogUser)
    picture = models.ImageField(upload_to='media/', default='icons8-гастробар-96.png', null=True, blank=True)
    name = models.CharField(max_length=32, unique=False,null=True, blank=True)
    posts = models.ManyToManyField(Post_for_Coincidence)
    def __str__(self):
        #return self.name
        return (f'{self.name}')

#название магазина
class Shop(models.Model):
    #Id не надо, он уже сам появиться
    name = models.CharField(max_length= 32, unique=True)
    def __str__(self):
        return self.name
class Merchandise(TimeStamp):
    good = models.CharField(max_length= 32)
    name = models.TextField()
    imageUrl = models.URLField()
    priceBefore = models.FloatField()
    priceAfter = models.FloatField()
    amount = models.FloatField()
    discount = models.IntegerField()
    market_name = models.CharField(max_length= 32)
    # Связь с категорией
    # один ко многим
    market = models.ForeignKey(Shop, on_delete= models.CASCADE)
    #image = models.ImageField(upload_to='posts', null=True, blank=True)
    user = models.ForeignKey(BlogUser, on_delete=models.CASCADE)
    def __str__(self):
        return ("{0:2d}% скидка в магазине {1} на товар: {2}.".format(self.discount, self.market_name, self.name))
    def fill_base_from_file(self, superuser, city, shop, xlsx):
        user = superuser[0]
        lenta = ED(CITY=city, SHOP=shop)  # создаем экземпляр класса
        lenta.load_xlsx(xlsx)  # загружаем интересующие нас товары из файла
        # сохраняем список интересующих нас товаров в базу через ORM
        for item in lenta.excel_data_df.name:
            good, created = Good.objects.get_or_create(name=item, user = user)
        lenta.get_df_discount()  # запрашиваем список товаров со скидками с сайта
        data_frame = pd.DataFrame()
        # сопоставляем искомые товары с перечнем скидок и сохраняем в базу
        if lenta.df_res.empty:
            print(f'Магазин {lenta.shop} не предоставил скидки')
            return -2
        for good in lenta.excel_data_df.name:
            count = 0
            for good_discount in lenta.df_res.name:
                result = re.match(good, good_discount)
                if ((result is None) == False):
                    df = pd.DataFrame({
                    'count': [count],
                    'good': [good],
                    'name': [good_discount]})
                    data_frame = pd.concat([data_frame, df])
                count = count + 1
        if data_frame.empty:
            print(f'Магазин {lenta.shop} не предоставил скидки на данные товары')
            return -1
        data = data_frame.merge(lenta.df_res, on=['name'], how='left')

        data = data.drop_duplicates(subset=['name'])
        #data.to_excel(f"{self.shop}.xlsx", index=False)
        data = data.reset_index()
        #data_frame.to_excel("output2.xlsx", index=False)
        shop, created = Shop.objects.get_or_create(name=lenta.shop)
        for index, row in data.iterrows():
            print(row['good'],"-", row['name'])
            if (pd.isna(row['amount']) == True):
                row['amount'] = 0.0
            if (pd.isna(row['discount']) == True):
                row['discount'] = 0.0
            merch, created = Merchandise.objects.get_or_create(
                name=row['name'], good = row['good'], imageUrl = row['imageUrl'], priceBefore = row['priceBefore'],
                priceAfter=row['priceAfter'], amount=row['amount'], discount=row['discount'],
                startDate = row['startDate'], endDate = row['endDate'], market_name = lenta.shop, market = shop, user = user)
        print(f"Данные по {lenta.shop} выгружены в базу")
        return 0
    def fill_base(self, simple_user, city, shop):
        user = simple_user[0]
        lenta = ED(CITY=city, SHOP=shop)  # создаем экземпляр класса

        goods = Good.objects.filter(user = user)
        list_result = [entry.name for entry in goods]  # converts QuerySet into Python list
        data = {'name': list_result}
        lenta.excel_data_df = pd.DataFrame(data, columns=['name'])
        #lenta.load_xlsx(xlsx)  # загружаем интересующие нас товары из файла
        # сохраняем список интересующих нас товаров в базу через ORM
        for item in lenta.excel_data_df.name:
            good, created = Good.objects.get_or_create(name=item, user = user)
        lenta.get_df_discount()  # запрашиваем список товаров со скидками с сайта
        data_frame = pd.DataFrame()
        # сопоставляем искомые товары с перечнем скидок и сохраняем в базу
        if lenta.df_res.empty:
            print(f'Магазин {lenta.shop} не предоставил скидки')
            return -2
        for good in lenta.excel_data_df.name:
            count = 0
            for good_discount in lenta.df_res.name:
                result = re.match(good, good_discount)
                if ((result is None) == False):
                    df = pd.DataFrame({
                    'count': [count],
                    'good': [good],
                    'name': [good_discount]})
                    data_frame = pd.concat([data_frame, df])
                count = count + 1
        if data_frame.empty:
            print(f'Магазин {lenta.shop} не предоставил скидки на данные товары')
            return -1
        data = data_frame.merge(lenta.df_res, on=['name'], how='left')

        data = data.drop_duplicates(subset=['name'])
        #data.to_excel(f"{self.shop}.xlsx", index=False)
        data = data.reset_index()
        #data_frame.to_excel("output2.xlsx", index=False)
        shop, created = Shop.objects.get_or_create(name=lenta.shop)
        for index, row in data.iterrows():
            print(row['good'],"-", row['name'])
            if (pd.isna(row['amount']) == True):
                row['amount'] = 0.0
            if (pd.isna(row['discount']) == True):
                row['discount'] = 0.0
            merch, created = Merchandise.objects.get_or_create(
                name=row['name'], good = row['good'], imageUrl = row['imageUrl'], priceBefore = row['priceBefore'],
                priceAfter=row['priceAfter'], amount=row['amount'], discount=row['discount'],
                startDate = row['startDate'], endDate = row['endDate'], market_name = lenta.shop, market = shop, user = user)
        print(f"Данные по {lenta.shop} выгружены в базу")
        return 0

    @cached_property
    def get_max_discount_cached(self):
        print('max_discount_cached')
        max = Merchandise.objects.select_related('market', 'user').order_by('-discount')[:9]
        #max = Merchandise.objects.order_by('-discount')[:9]
        return max

    def get_max_discount(self):
        print('*******')
        max = Merchandise.objects.order_by('-discount')[:9]
        return max
def create_new_post(name = 'Рецепт',text = 'Подсолите', user = 'user', id = 0):
    print(f'функция.{name}.{text}.{user}.{id}')
    user = BlogUser.objects.filter(username=user)
    post = Post_for_Coincidence.objects.create(name = name, text =text,user = user[0])
    coincidence = Coincidence.objects.get(pk=id)
    coincidence.posts.add(post)
    #print(coincidence)

    #user = BlogUser.objects.filter(username=user)
    #coinc, created = Coincidence.objects.get_or_create(name = name)
    #coinc.users.add(user[0])
    #query = Good.objects.filter(name=name, user = user[0]).exists()
    query =True
    if query == True:
        #print(f'Уже существует')
        return False
    else:
        #print(f'Еще не было')
        return True











