# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-01-14 22:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppSklad', '0007_auto_20170114_0257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(max_length=150, verbose_name='Текст комментария'),
        ),
    ]
