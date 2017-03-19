#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from .models import Detail, Item, ItemDetails, Category, Profile, Comment
# from django.utils.translation import ugettext as _


GEN = (
    ('', '--Пол--'),
    ('Мужской', 'Мужской'),
    ('Женский', 'Женский'),
    )


"""********************************************** Форма для поиска **************************************************"""


class SearchForm(forms.ModelForm):

    class Meta:
        model = Detail
        fields = ('title',)


"""************************************** Форма для редактирования детали *******************************************"""


class DetailForm(forms.ModelForm):

    class Meta:
        model = Detail
        fields = ('title', 'category', 'price', 'count', 'color', 'image')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Название детали', 'class': 'detail_input'}),
            'category': forms.Select(attrs={'placeholder': 'Категория', 'class': 'detail_select'}),
            'price': forms.TextInput(attrs={'placeholder': 'Цена за единицу', 'class': 'detail_input_elem'}),
            'count': forms.TextInput(attrs={'placeholder': 'Количество', 'class': 'detail_input_elem'}),
            'color': forms.Select(attrs={'placeholder': 'Цвет', 'class': 'detail_select'}),
        }


"""************************************** Форма для редактирования товара *******************************************"""


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ('author', 'category', 'title', 'price', 'image')
        widgets = {
            'author': forms.TextInput(attrs={'placeholder': 'Автор', 'class': 'detail_input'}),
            'title': forms.TextInput(attrs={'placeholder': 'Название товара', 'class': 'detail_input'}),
            'category': forms.Select(attrs={'class': 'detail_select'}),
            'price': forms.TextInput(attrs={'id': 'id_price1', 'placeholder': 'Цена', 'class': 'item_input_elem'}),
        }


"""************************************** Форма для редактирования товара *******************************************"""


class ItemDetailsForm(forms.ModelForm):

    class Meta:
        model = ItemDetails
        fields = ('item', 'detail', 'detail_count')
        widgets = {
            'detail': forms.Select(attrs={'class': 'item_input'}),
            'detail_count': forms.TextInput(attrs={'placeholder': 'шт.', 'class': 'item_input_count'}),
        }

    # def __init__(self, *args, **kwargs):
    #     super(ItemDetailsForm, self).__init__(*args, **kwargs)
    #     if self.instance:
    #         self.fields['detail'].queryset = Detail.objects.filter(
    #             category__pk=self.instance.detail.category.pk)


"""***************************************** Форма для создания категории *******************************************"""


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('title', 'title_plural')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Название категории', 'class': 'detail_input'}),
            'title_plural': forms.TextInput(attrs={'placeholder': 'Название во мн.ч.',
                                                   'class': 'detail_input'}),
        }


"""***************************************** Форма профиля пользователя *********************************************"""


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


"""*************************************** Форма доп. профиля пользователя ******************************************"""


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('gender', 'birth_date', 'image', 'register_date', 'remember', 'last_seen')


"""************************************* Форма изменения профиля пользователя ***************************************"""


class UserFormEdit(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Имя', 'class': 'change_password_input'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Фамилия', 'class': 'change_password_input'}),
            'email': forms.TextInput(attrs={'placeholder': 'Почта', 'class': 'change_password_input'}),
        }


"""*********************************** Форма доп. изменения профиля пользователя ************************************"""


class ProfileFormEdit(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('gender', 'birth_date', 'image')
        widgets = {
            'gender': forms.Select(attrs={'placeholder': 'Пол', 'class': 'change_password_input'}, choices=GEN),
            'birth_date': forms.DateInput(attrs={'placeholder': 'Дата рождения (01.01.2001)',
                                                 'class': 'change_password_input'}),
        }

    image = forms.ImageField(required=False, label='photo')


"""********************************************** Форма смены пароля ************************************************"""


class UserFormChangePassword(forms.Form):
    password_ch = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'Новый пароль',
                                                                                   'class': 'change_password_input'}))
    password_ch_new = forms.CharField(max_length=50,
                                      widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль',
                                                                        'class': 'change_password_input'}))


"""********************************************** Форма комментария *************************************************"""


class CommentFormEdit(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows': '10', 'placeholder': 'Введите комментарий', 'class': 'comment_edit'}),
        }