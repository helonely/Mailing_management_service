from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')

    avatar = models.ImageField(upload_to='users/avatars/', verbose_name='Аватар', blank=True, null=True, help_text='Загрузите ваш аватар')
    phone = models.CharField(max_length=30, verbose_name='Телефон', blank=True, null=True, help_text='Введите номер телефона')
    country = models.CharField(max_length=30, verbose_name='Страна', blank=True, null=True)

    token = models.CharField(max_length=255, verbose_name='Token', blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
