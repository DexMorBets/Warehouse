#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms


"""********************************************** Форма для поиска **************************************************"""


class RememberForm(forms.Form):
    remember_me = forms.BooleanField()