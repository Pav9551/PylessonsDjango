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



