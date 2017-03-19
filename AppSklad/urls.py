#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^goods/(?P<pk>[0-9]+)/publicate/$', views.publicate_item, name='publicate_item'),
    url(r'^goods/(?P<pk>[0-9]+)/unpublicate/$', views.unpublicate_item, name='unpublicate_item'),
    url(r'^goods/(?P<pk>[0-9]+)/$', views.item_detail, name='item_detail'),
    url(r'^goods/[0-9]+/comment/delete/$', views.comment_delete, name='comment_delete'),
    url(r'^goods/edit/(?P<pk>[0-9]+)/$', views.item_edit, name='item_edit'),
    url(r'^goods/edit/delete/(?P<pk>[0-9]+)/$', views.item_delete, name='item_delete'),
    url(r'^goods/category/(?P<category_value>[А-я]+)/$', views.goods_list, name='category_list'),
    url(r'^goods/$', views.goods_list, name='goods_list'),
    url(r'^goods/(?P<category>[А-я]+)/newitem/$', views.item_new, name='item_new'),
    # url(r'^goods/new/$', views.item_new, name='item_new'),
    url(r'^goods/profit/(?P<category>[А-я]+)/$', views.item_profit, name='item_profit'),
    url(r'^goods/profit/items/$', views.item_profit, name='items_profit'),
    url(r'^details/page/(\d+)/$', views.details_list, name='details_list'),
    url(r'^details/(?P<pk>[0-9]+)/$', views.details_detail, name='details_detail'),
    url(r'^details/edit/(?P<pk>[0-9]+)/$', views.detail_edit, name='detail_edit'),
    url(r'^details/(?P<pk>[0-9]+)/delete/$', views.detail_delete, name='detail_delete'),
    url(r'^details/new/$', views.detail_new, name='detail_new'),
    url(r'^details/$', views.details_list, name='details_list'),
    url(r'^goods/category/new/$', views.category_new, name='category_new'),
    url(r'^goods/category/delete/$', views.category_delete, name='category_delete'),
    url(r'^user/change_password/$', views.change_password, name='change_password'),
    url(r'^user/edit/$', views.user_edit, name='user_edit'),
    url(r'^user/[A-z,0-9]+/comments/[0-9]+/comment/delete/$', views.comment_delete, name='comment_delete'),
    url(r'^user/(?P<username>[A-z,0-9]+)/comments/$', views.user_comments, name='user_comments'),
    url(r'^user/(?P<username>[A-z,0-9]+)/goods/$', views.user_items, name='user_items'),
    url(r'^user/(?P<username>[A-z,0-9]+)/$', views.user_profile, name='user_profile'),
    url(r'^', views.details_list, name='details_list'),

]