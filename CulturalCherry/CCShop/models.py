from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    product_name = models.CharField(max_length=50, verbose_name='Название')
    foto = models.ImageField(upload_to='images/', verbose_name='Фото')
    price = models.IntegerField(verbose_name='Цена')
    sex = models.ForeignKey('Sex', on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)


class Sex(models.Model):
    sex = models.CharField(max_length=30, null=False, verbose_name='Пол')


class Category(models.Model):
    category_name = models.CharField(max_length=30, null=False, verbose_name='Название категории')


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=False)
    count = models.IntegerField(verbose_name='Количество')

