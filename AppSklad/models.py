#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
# from django.utils.translation import ugettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, verbose_name='Пол', blank=True)
    birth_date = models.DateField(verbose_name='Дата рождения', null=True, blank=True)
    register_date = models.DateField(verbose_name='Дата регистрации', null=True, blank=True)
    last_seen = models.DateField(verbose_name='Дата последнего посещения', null=True, blank=True)
    remember = models.BooleanField(verbose_name='Запомнить', default=False)
    image = models.ImageField(upload_to='avatars/%Y/%m/%d/', blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Detail(models.Model):
    class Meta:
        verbose_name = 'Деталь'
        verbose_name_plural = 'Детали'

    title = models.CharField(verbose_name='Название детали', max_length=200)
    category = models.ForeignKey('Category', verbose_name='Категория детали', related_name='+', default='')
    price = models.IntegerField(verbose_name='Закупочная цена')
    count = models.IntegerField(verbose_name='Количество')
    color = models.ForeignKey('Color', verbose_name='Цвет', related_name='+', default='', null=True, blank=True)
    image = models.ImageField(upload_to='details/%Y/%m/%d/', blank=True)

    def __str__(self):
        if self.color:
            return self.title + " " + "|" + self.category.title + " " + "|" + self.color.title
        else:
            return self.title + " " + "|" + self.category.title


class Category(models.Model):
    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'

    title = models.CharField(verbose_name='Название категории', max_length=50)
    title_plural = models.CharField(verbose_name='Название категории во множественном числе', max_length=50)
    item_count = models.IntegerField(verbose_name='Количесвто товаров в категории', blank=True, null=True)

    def __str__(self):
        return self.title_plural


class Item(models.Model):
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    author = models.ForeignKey(User, verbose_name='Автор', related_name="items", default='', blank=True, null=True)
    category = models.ForeignKey('Category', verbose_name='Категория товара', related_name='+', default='')
    title = models.CharField(verbose_name='Название модели', max_length=50)
    price = models.IntegerField(verbose_name='Отпускная цена')

    expenses = models.IntegerField(verbose_name='Затраты на изготовление', null=True, blank=True)
    available = models.IntegerField(verbose_name='Количетсво достпных', null=True, blank=True)
    profit = models.IntegerField(verbose_name='Прибыль', null=True, blank=True)
    image = models.ImageField(upload_to='items/%Y/%m/%d/', blank=True)
    publicate = models.BooleanField(verbose_name='Публикация', default=False)

    def publicate_item(self):
        self.publicate = True
        self.save()

    def unpublicate_item(self):
        self.publicate = False
        self.save()

    def __str__(self):
        return self.category.title + " " + self.title


class ItemDetails(models.Model):
    class Meta:
        verbose_name = 'Деталь товара'
        verbose_name_plural = 'Детали товаров'

    item = models.ForeignKey('Item', verbose_name='Товар', related_name='itemdetails')
    detail = models.ForeignKey('Detail', verbose_name='Деталь', related_name='+')
    detail_count = models.IntegerField(verbose_name='Количество деталей')

    def __str__(self):
        return self.item.category.title + " " + self.item.title + " " + self.detail.title

    def get_category_detail(self, category):
        return self.detail.filter(category=category)


class Comment(models.Model):
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    item = models.ForeignKey('Item', verbose_name='Товар', related_name="comments")
    author = models.ForeignKey(User, verbose_name='Автор', related_name="comments")
    text = models.TextField(max_length=150, verbose_name='Текст комментария')
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text


class Color(models.Model):
    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'

    title = models.CharField(verbose_name='Цвет', max_length=100)
    code = models.CharField(verbose_name='Код', max_length=25)

    def __str__(self):
        return self.title