from django.conf import settings
from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='порода')
    description = models.TextField(verbose_name='описание', **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'порода'
        verbose_name_plural = 'породы'


class Dog(models.Model):
    name = models.CharField(max_length=150, verbose_name='кличка')
    category = models.ForeignKey(Category, max_length=150, verbose_name='порода', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='dogs/', verbose_name='фото', **NULLABLE)
    birth_date = models.DateField(verbose_name='дата рождения', **NULLABLE)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='владелец')

    def __str__(self):
        return f'{self.name}({self.category})'

    class Meta:
        verbose_name = 'собака'
        verbose_name_plural = 'собаки'


class Parent(models.Model):
    dog = models.ForeignKey(Dog, verbose_name='потомок', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='кличка', max_length=75)
    category = models.ForeignKey(Category, max_length=150, verbose_name='порода', on_delete=models.CASCADE)
    birth_date = models.DateField(verbose_name='дата рождения', **NULLABLE)

    def __str__(self):
        return f'{self.name} ({self.category})'

    class Meta:
        verbose_name = 'предок'
        verbose_name_plural = 'предки'





