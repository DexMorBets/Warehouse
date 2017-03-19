#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Detail, Category, Item, ItemDetails, Comment, Color


class ItemDetailInline(admin.TabularInline):
    model = ItemDetails
    extra = 3


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 3


class ItemAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Основное', {'fields': [('category', 'title', 'author')]}),
        ('Отпускная цена', {'fields': ['price']}),
        ('Прочее', {'fields': ['expenses', 'available',
                               'profit', 'publicate'],
                    'classes': ['collapse']}),
    ]
    inlines = [ItemDetailInline, CommentInline]

admin.site.unregister(Group)
admin.site.register(Detail)
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Item, ItemAdmin)
