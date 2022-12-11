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
