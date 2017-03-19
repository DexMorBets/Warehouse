from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [

    url(r'^login/register/', views.register, name='register'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),

]