# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-01-12 00:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Название категории')),
                ('title_plural', models.CharField(max_length=50, verbose_name='Название категории во множественном числе')),
                ('item_count', models.IntegerField(blank=True, null=True, verbose_name='Количесвто товаров в категории')),
            ],
            options={
                'verbose_name': 'Категория товара',
                'verbose_name_plural': 'Категории товаров',
            },
        ),
        migrations.CreateModel(
            name='Detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название детали')),
                ('price', models.IntegerField(verbose_name='Закупочная цена')),
                ('count', models.IntegerField(verbose_name='Количество')),
                ('category', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='AppSklad.Category', verbose_name='Категория детали')),
            ],
            options={
                'verbose_name': 'Деталь',
                'verbose_name_plural': 'Детали',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Название модели')),
                ('price', models.IntegerField(verbose_name='Отпускная цена')),
                ('expenses', models.IntegerField(blank=True, null=True, verbose_name='Затраты на изготовление')),
                ('available', models.IntegerField(blank=True, null=True, verbose_name='Количетсво достпных')),
                ('profit', models.IntegerField(blank=True, null=True, verbose_name='Прибыль')),
                ('category', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='AppSklad.Category', verbose_name='Категория товара')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='ItemDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail_count', models.IntegerField(verbose_name='Количество деталей')),
                ('detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='AppSklad.Detail', verbose_name='Деталь')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='AppSklad.Item', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Деталь товара',
                'verbose_name_plural': 'Детали товаров',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(blank=True, max_length=10, verbose_name='Пол')),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
