from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    product_name = models.CharField(max_length=50, verbose_name='Название')
    foto = models.ImageField(upload_to='images/', verbose_name='Фото', null=True, blank=True)
    price = models.IntegerField(verbose_name='Цена')
    sex = models.ForeignKey('Sex', on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Sex(models.Model):
    sex = models.CharField(max_length=30, null=False, verbose_name='Пол')

    def __str__(self):
        return self.sex

    class Meta:
        verbose_name = 'Пол'
        verbose_name_plural = 'Полы'


class Category(models.Model):
    category_name = models.CharField(max_length=30, null=False, verbose_name='Название категории')

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=False)
    count = models.IntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
