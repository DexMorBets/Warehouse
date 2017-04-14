# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-01-15 21:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('AppSklad', '0012_auto_20170115_0545'),
    ]

    operations = [
        migrations.AddField(
            model_name='detail',
            name='image',
            field=models.ImageField(blank=True, upload_to='details/%Y/%m/%d/'),
        ),
        migrations.AddField(
            model_name='item',
            name='author',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, upload_to='items/%Y/%m/%d/'),
        ),
    ]
