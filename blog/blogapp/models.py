from django.db import models

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
class Good(models.Model):
    name = models.CharField(max_length=32, unique=True)
    def __str__(self):
        return self.name
#название магазина
class Shop(models.Model):
    #Id не надо, он уже сам появиться
    name = models.CharField(max_length= 32, unique=True)
    def __str__(self):
        return self.name
class Merchandise(models.Model):
    good = models.CharField(max_length= 32)
    name = models.TextField()
    imageUrl = models.URLField()
    priceBefore = models.FloatField()
    priceAfter = models.FloatField()
    amount = models.FloatField()
    discount = models.IntegerField()
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    market_name = models.CharField(max_length= 32)
    # Связь с категорией
    # один ко многим
    market = models.ForeignKey(Shop, on_delete= models.CASCADE)
    def __str__(self):
        return ("{0:2d}% скидка в магазине {1} на товар: {2}.".format(self.discount, self.market_name, self.name))






