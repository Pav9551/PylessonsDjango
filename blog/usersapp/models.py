from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class BlogUser(AbstractUser):

    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)

    # Переопределение метода save
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Создаем профиль
        # Если провиль не создан
        if not Profile.objects.filter(user=self).exists():
            Profile.objects.create(user=self)


class Profile(models.Model):
    # При создании пользователя создать Profile
    info = models.TextField(blank=True)
    user = models.OneToOneField(BlogUser, on_delete=models.CASCADE)
