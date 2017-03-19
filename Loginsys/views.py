# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.template.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from AppSklad.forms import ProfileForm
from django.utils import timezone
from .forms import RememberForm


"""**************************************** Аутентификация пользователя *********************************************"""


def login(request):
    args = {}
    args.update(csrf(request))
    form = RememberForm()
    if request.POST:
        # newform = RememberForm(request.POST)
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        # if newform['remember_me']:
        #     request.session['remember_me'] = newform['remember_me']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            args['login_error'] = 'Пользователя с такими именем не существует, либо пароль указан неверно.'
            return render_to_response('login.html', args)

    else:
        args['form'] = form
        return render_to_response('login.html', args)


"""********************************************** Выход пользователя ************************************************"""


def logout(request):
    auth.logout(request)
    return redirect('/')


"""***************************************** Регистрация пользователя ***********************************************"""


def register(request):
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm()
    args['profile_form'] = ProfileForm()
    if request.POST:
        newuser_form = UserCreationForm(request.POST)
        profile_user = ProfileForm(request.POST)
        if newuser_form.is_valid() and profile_user.is_valid():
            newuser_form.save()
            newuser = auth.authenticate(username=newuser_form.cleaned_data['username'],
                                        password=newuser_form.cleaned_data['password2'])
            newuser.profile.register_date = timezone.now()
            newuser.profile.save()
            auth.login(request, newuser)
            return redirect('/')
        else:
            args['form'] = newuser_form
            args['profile_form'] = profile_user
    return render_to_response('register.html', args)
