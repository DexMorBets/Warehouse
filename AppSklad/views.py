# coding=utf-8
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test
from .models import Detail, Category, Comment, User
from django.core.paginator import Paginator
from django.template.context_processors import csrf
from django.http import HttpResponse
from .forms import SearchForm, DetailForm, ItemForm, ItemDetailsForm, CategoryForm, UserForm, UserFormChangePassword,\
    UserFormEdit, ProfileForm, ProfileFormEdit, CommentFormEdit
from .models import Item, ItemDetails
from datetime import datetime
from django.db.models import Count
import json


"""**************************************** Отображение списка деталей **********************************************"""


def details_list(request, page_number=1):
    args = {}
    args.update(csrf(request))
    if request.user.is_authenticated():
        request.user.profile.last_seen = timezone.now()
        request.user.profile.save(update_fields=['last_seen'])
    if request.GET and len(request.GET.get('title')) > 0:
        newuser_form = SearchForm(request.GET)
        all_details = Detail.objects.filter(title__contains=request.GET.get('title')).\
            values('id', 'title', 'category__title_plural', 'price', 'count', 'color__title', 'color__code').\
            order_by('category__title', 'title')
        args['form'] = newuser_form
        args['new_details'] = all_details
        args['pg'] = False
    else:
        all_details = Detail.objects.all().values('id', 'title', 'category__title_plural', 'price', 'count',
                                                  'color__title', 'color__code').order_by('category__title_plural',
                                                                                          'title')
        current_page = Paginator(all_details, 10)
        args['new_details'] = current_page.page(page_number)
        count = all_details.count()
        args['pg'] = True
        args['count'] = count
    args['address'] = {'Детали': '/'}
    return render(request, 'sklad/details_list.html', args)


"""**************************************** Отображение списка товаров **********************************************"""


# функция расчёта количества доступных товаров
def available_goods(item_details, details):
    dict = {}
    max = 0
    for detail in details:
        dict[detail['title']] = detail['count']
        if detail['count'] > max:
            max = detail['count']
    minim = max
    for detail in item_details:
        current = dict[detail['detail__title']] // detail['detail_count']
        if current < minim:
            minim = current
    return minim


def goods_list(request, category_value=None, username=None):
    args = {}
    address = {}
    address_list = []
    address['Товар'] = '/goods/'
    address_list.append('Товар')
    categories = Category.objects.all().values('id', 'title_plural', 'item_count').order_by('-item_count')
    all_items_args = {'publicate': True}
    if category_value is None:
        unpubliched_items_args = {'publicate': False}
    else:
        all_items_args['category__title_plural'] = category_value
    if username:
        all_items_args['author__username'] = username
        address[username] = '/user/' + str(User.objects.filter(username=username).values_list('username', flat=True)[0]) + '/'
        address_list.append(username)
        if category_value is None:
            unpubliched_items_args['author__username'] = username
    if request.GET and len(request.GET.get('title')) > 0:
        all_items_args['title__contains'] = request.GET.get('title')
        if category_value is None:
            unpubliched_items_args['title__contains'] = request.GET.get('title')
    all_items = Item.objects.all().values('category__id', 'id', 'category__title', 'title',
                                          'expenses', 'price', 'profit', 'available').\
                                           filter(**all_items_args).order_by("title")
    if category_value is None:
        unpubliched_items = Item.objects.all().values('id', 'category__title', 'title', 'author__username', 'price').\
                                               filter(**unpubliched_items_args).order_by("category", "title")
        unpubliched_count = unpubliched_items.count()
        for unpubliched_item in unpubliched_items:
            unpubliched_item['comments_count'] = Item.objects.get(id=unpubliched_item['id']).item_comments.all().count()
        args['unpubliched_items'] = unpubliched_items
        args['unpubliched_count'] = unpubliched_count
    else:
        address[category_value] = '/goods/category/' + category_value + '/'
        address_list.append(category_value)
    for item in all_items:
        item['comments_count'] = Item.objects.get(id=item['id']).item_comments.all().count()
    args['category_value'] = category_value

    # получение данных о количестве товаров в каждой категории
    if username:
        args['username'] = username
    if request.GET and len(request.GET.get('title')) > 0:
        new_form = SearchForm(request.GET)
        args['search'] = True
        args['form'] = new_form
    if username or (request.GET and len(request.GET.get('title')) > 0):
        categories = [x for x in categories if x['item_count'] != 0]
    else:
        args['search'] = False
    args['categories'] = categories
    args['all_items'] = all_items
    args['address'] = address
    args['address_list'] = address_list
    if category_value is None:
        return render(request, 'sklad/goods_list.html', args)
    else:
        return render(request, 'sklad/category_list.html', args)


"""**************************************** Расчёт максимальной прибыли *********************************************"""


def profit_available_goods(all_items, dict_details):
    sum_min = 0
    for i in range(len(all_items)):
        item_details = ItemDetails.objects.values('detail__id', 'detail_count').filter(item_id=all_items[i]['id'])
        min = 15000
        for detail in item_details:
            current = dict_details[detail['detail__id']] // detail['detail_count']
            if current < min:
                if current < 0:
                    min = 0
                else:
                    min = current
        sum_min += min
        all_items[i]['available'] = min
    if sum_min == 0:
        return False
    return all_items


def item_profit(request, category=None):
    args = {}
    address = {}
    address_list = []
    list_of_items = []
    sum_profit = 0
    address['Прибыль'] = '/goods/profit/items/'
    address_list.append('Прибыль')

    if category:
        all_items = Item.objects.all().values('id', 'available', 'profit', 'expenses', 'category__title', 'title').filter(category__title_plural=category, publicate=True, profit__gt=0).order_by("title")  # набор всех товаров
        details = Detail.objects.all().values('id', 'count', 'title', 'category__title').filter(category__title_plural=category).order_by("title")  # набор всех деталей
        args['category'] = category
        address[category] = '/goods/category/' + category + '/'
        address_list.append(category)
    else:
        all_items = Item.objects.all().values('id', 'available', 'profit', 'expenses', 'category__title', 'title').filter(publicate=True, profit__gt=0).order_by("title")  # набор всех товаров
        args['all_items'] = all_items
        details = Detail.objects.all().values('id', 'count', 'title', 'category__title').order_by("title")  # набор всех деталей
    dict_details = {detail['id']: detail['count'] for detail in details}  # словать деталей
    while True:

        max_profit = 0
        max_profit_item = None

        # поиск самого выгодного товара
        all_items = profit_available_goods(all_items, dict_details)
        if not all_items:
            break
        for item in all_items:
            prof = item['available']*item['profit']
            if prof > max_profit:
                max_profit = prof
                max_profit_item = item  # сохранение объекта самого выгодного товара
            if max_profit_item is None:
                break

        if max_profit_item is None:
            break

        max_profit_item_details = ItemDetails.objects.values('detail__id', 'detail_count').filter(item_id=max_profit_item['id'])  # набор деталей выбранного товара

        # вычисление остатка деталей, после происзводства доступного количества данного товара
        for detail in max_profit_item_details:
            dict_details[detail['detail__id']] -= detail['detail_count']*max_profit_item['available']

        # удаление товара
        all_items.exclude(id=max_profit_item['id'])
        max_profit_item['count'] = max_profit_item['available']
        max_profit_item['received'] = (max_profit_item['available'] * max_profit_item['profit']) +\
                                      (max_profit_item['available'] * max_profit_item['expenses'])
        max_profit_item['profit'] = max_profit_item['available'] * max_profit_item['profit']
        max_profit_item['expenses'] = max_profit_item['available'] * max_profit_item['expenses']
        list_of_items.append(max_profit_item)
        sum_profit += max_profit_item['profit']

        # проверка на количество оставшихся деталей
        if len(all_items) == 0:
            break
    for detail in details:
        detail['count'] = dict_details[detail['id']]
    for item in list_of_items:
        item['comments_count'] = Item.objects.get(id=item['id']).item_comments.all().count()
    args['list_of_items'] = list_of_items
    args['details'] = details
    args['sum_profit'] = sum_profit
    args['dict_details'] = dict_details
    args['address'] = address
    args['address_list'] = address_list
    return render(request, 'sklad/goods_profit.html', args)


"""*************************************** Детальная информация о товаре *******************************************"""


def item_detail(request, pk):
    args = {}
    address = {}
    address_list = []
    item = get_object_or_404(Item, pk=pk)
    item_values = Item.objects.filter(id=pk).values('id', 'author__id', 'title', 'category__title', 'image',
                                                    'author__username', 'price', 'publicate')[0]
    itemdetails = item.itemdetails.all().values('detail__color__code', 'detail__id', 'detail__title', 'detail_count')
    itemcomments = item.item_comments.all().values('author__username', 'id', 'author__profile__image', 'created_date',
                                                   'text', 'author__id')
    category_items = list(Item.objects.filter(category__title=item_values['category__title']).\
                          order_by('category__title', 'title').only('id'))
    current = category_items.index(item)
    if current-1 >= 0:
        args['previous'] = category_items[current-1].id
    if current+1 <= len(category_items)-1:
        args['next'] = category_items[current+1].id
    if request.method == "POST":
        form = CommentFormEdit(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = auth.get_user(request)
            comment.item = item
            comment.created_date = timezone.now()
            comment.save()
            return redirect('item_detail', pk=item.pk)
    else:
        form = CommentFormEdit()
    args['itemdetails'] = itemdetails
    args['item_values'] = item_values
    args['form'] = form
    args['itemcomments'] = itemcomments
    address['Товар'] = '/goods/'
    address_list.append('Товар')
    address[item_values['category__title'] + ' ' + item_values['title']] = '/goods/' + pk + '/'
    address_list.append(item_values['category__title'] + ' ' + item_values['title'])
    args['address'] = address
    args['address_list'] = address_list
    return render(request, 'item_detail.html', args)


"""*************************************** Редактирование товара ****************************************************"""


@login_required
def item_edit(request, pk):
    args = {}
    address = {}
    address_list = []
    item = get_object_or_404(Item, pk=pk)
    item_values = Item.objects.all().values('id', 'title', 'category__title', 'image', 'category__id').get(pk=pk)
    itemDetailsFormSet = inlineformset_factory(Item, ItemDetails, form=ItemDetailsForm, fk_name='item', fields=('detail', 'detail_count'), max_num=11, extra=8)
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, instance=item)
        formset = itemDetailsFormSet(request.POST, instance=item)
        for form1 in formset:
            form1.fields['detail'].queryset = Detail.objects.filter(category__id=item_values['category__id'])
        if form.is_valid() and formset.is_valid():
            title = Item.objects.filter(title=form.cleaned_data['title'], category=form.cleaned_data['category']).exists()
            if title and item.title != form.cleaned_data['title']:
                args['error'] = 'Товар с таким именем уже существует!'
                form = ItemForm(instance=item)
                formset = itemDetailsFormSet(instance=item)
            else:
                new_form = form.save(commit=False)
                new_form.price = form.cleaned_data['price']
                new_form.category = form.cleaned_data['category']
                new_form.title = form.cleaned_data['title']
                new_form.author = auth.get_user(request)
                new_form.save()
                formset.save()
                details = Detail.objects.all().values('count', 'title')
                expenses = 0

                # получение деталей, использованных для данного товара
                item_details = ItemDetails.objects.values('detail__price', 'detail_count', 'detail__title').filter(item__id=item_values['id'])

                # расчёт затрат данного товара
                if item_details:
                    for detail in item_details:
                        expenses += detail['detail__price'] * detail['detail_count']
                    item.available = available_goods(item_details, details)
                    item.expenses = expenses
                    item.profit = item.price - expenses
                    item.save(update_fields=['available', 'expenses', 'profit'])
                return redirect('item_detail', pk=item_values['id'])
        else:
            form = ItemForm(instance=item)
            formset = itemDetailsFormSet(instance=item)
            for form1 in formset:
                form1.fields['detail'].queryset = Detail.objects.filter(category__id=item_values['category__id'])
    else:
        formset = itemDetailsFormSet(instance=item)
        form = ItemForm(instance=item)
        for form1 in formset:
            form1.fields['detail'].queryset = Detail.objects.filter(category__id=item.category.id)
    args['formset'] = formset
    args['form'] = form
    args['item_image'] = item_values['image']
    address['Товар'] = '/goods/'
    address_list.append('Товар')
    address[item_values['category__title'] + ' ' + item_values['title']] = '/goods/' + pk + '/'
    address_list.append(item_values['category__title'] + ' ' + item_values['title'])
    address['Редактирование товара'] = request.get_full_path()
    address_list.append('Редактирование товара')
    args['address'] = address
    args['address_list'] = address_list
    return render(request, 'item_edit.html', args)


"""********************************************* Удаление товара ****************************************************"""


@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    item.delete()
    return redirect('goods_list')


"""********************************************* Создание товара ****************************************************"""


@login_required
def item_new(request, category=None):
    args = {}
    address = {}
    address_list = []
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            title = Item.objects.filter(title=form.cleaned_data['title'], category=form.cleaned_data['category']).exists()
            if title:
                args['error'] = 'Товар с таким именем уже существует!'
                form = ItemForm(request.POST)
            else:
                new_form = form.save(commit=False)
                new_form.author = auth.get_user(request)
                new_form.save()
                return redirect("item_edit", pk=new_form.pk)
        else:
            form = ItemForm(request.POST)
    else:

        form = ItemForm()
    args['form'] = form
    if category:
        args['category'] = category
    address['Товар'] = '/goods/'
    address_list.append('Товар')
    address['Новый товар'] = request.get_full_path()
    address_list.append('Новый товар')
    args['address'] = address
    args['address_list'] = address_list
    return render(request, 'item_edit.html', args)


"""************************************** Детальная информация о детали *********************************************"""


def details_detail(request, pk):
    args = {}
    address = {}
    address_list = []
    model = Detail.objects.filter(id=pk).values('id', 'title', 'category__title_plural', 'category__title', 'price',
                                                'count', 'color__title', 'color__code', 'image')
    detail = get_object_or_404(model, id=pk)
    args['detail'] = detail
    address['Детали'] = '/'
    address_list.append('Детали')
    address[model[0]['title']] = request.get_full_path()
    address_list.append(model[0]['title'])
    args['address'] = address
    args['address_list'] = address_list
    return render(request, 'details_detail.html', args)


"""*************************************** Редактирование детали ****************************************************"""


@login_required
def detail_edit(request, pk):
    args = {}
    address = {}
    address_list = []
    detail = get_object_or_404(Detail, id=pk)
    if request.method == "POST":
        form = DetailForm(request.POST, request.FILES, instance=detail)
        if form.is_valid():
            title = Detail.objects.filter(title=form.cleaned_data['title']).exists()
            if title and detail.title != form.cleaned_data['title']:
                args['error'] = 'Деталь с таким именем уже существует!'
                form = DetailForm(request.POST)
            else:
                detail = form.save()
                return redirect('details_detail', pk=detail.pk)
    else:
        form = DetailForm(instance=detail)
    args['form'] = form
    args['detail_image'] = detail.image
    address['Детали'] = '/'
    address_list.append('Детали')
    address[detail.title] = '/details/' + pk + '/'
    address_list.append(detail.title)
    address['Редактирование детали'] = request.get_full_path()
    address_list.append('Редактирование детали')
    args['address'] = address
    args['address_list'] = address_list
    return render(request, 'detail_edit.html', args)


"""*************************************** Создание новой детали ****************************************************"""


@login_required
def detail_new(request):
    args = {}
    address = {}
    address_list = []
    new = True
    if request.method == "POST":
        form = DetailForm(request.POST, request.FILES)
        if form.is_valid():
            title = Detail.objects.filter(title=form.cleaned_data['title']).exists()
            if title:
                args['error'] = 'Деталь с таким именем уже существует!'
                form = DetailForm(request.POST)
            else:
                detail = form.save(commit=False)
                detail.save()
                return redirect('details_detail', pk=detail.pk)
    else:
        form = DetailForm()
    args['form'] = form
    args['new'] = new
    address['Детали'] = '/'
    address_list.append('Детали')
    address['Новая деталь'] = request.get_full_path()
    address_list.append('Новая деталь')
    args['address'] = address
    args['address_list'] = address_list
    return render(request, 'detail_edit.html', args)


"""********************************************* Удаление детали ****************************************************"""


@login_required
def detail_delete(request, pk):
    detail = get_object_or_404(Detail, pk=pk)
    detail.delete()
    return redirect('details_list')


""""************************************** Создание новой категории *************************************************"""


@login_required
def category_new(request):
    args = {}
    address = {}
    address_list = []
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            title = Category.objects.filter(title=form.cleaned_data['title']).exists()
            title_plural = Category.objects.filter(title_plural=form.cleaned_data['title_plural']).exists()
            if title or title_plural:
                args['error'] = 'Такая категория уже существует!'
                form = CategoryForm(request.POST)
            else:
                newform = form.save()
                cat = Category.objects.get(id=newform.id)
                cat.item_count = 0
                cat.save()
                return redirect('goods_list')
    else:
        form = CategoryForm()
    args['form'] = form
    address['Новая категория'] = request.get_full_path()
    address_list.append('Новая категория')
    args['address'] = address
    args['address_list'] = address_list
    return render(request, 'category_new.html', args)


""""****************************************** Удаление категории ***************************************************"""


@login_required
def category_delete(request):
    if request.method == "POST":
        title = request.POST['title']
        category = get_object_or_404(Category, title_plural=title)
        category.delete()
    return HttpResponse('Ок')


""""****************************************** Удаление комментария *************************************************"""


@login_required
def comment_delete(request):
    if request.method == "POST" and request.is_ajax():
        pk = request.POST['pk']
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
    return HttpResponse("ok")


""""****************************************** Профиль пользователя *************************************************"""


@login_required
def user_profile(request, username):
    args = {}
    address = {}
    address_list = []
    user = User.objects.get(username=username)
    user_comments_count = user.author_comments.all().count()
    user_form = UserForm(instance=user)
    profile_user = ProfileForm(instance=user.profile)
    admin = user.is_superuser
    args['admin'] = admin
    args['user_form'] = user_form
    args['user_object'] = user
    args['user_comments_count'] = user_comments_count
    args['profile_user'] = profile_user
    address[user.username] = request.get_full_path()
    address_list.append(user.username)
    args['address'] = address
    args['address_list'] = address_list
    return render(request, 'user_profile.html', args)


""""********************************************** Смена ппароля ****************************************************"""


@login_required
def change_password(request):
    args = {}
    address = {}
    address_list = []
    user = request.user
    if request.method == "POST":
        form = UserFormChangePassword(request.POST)
        if form.is_valid():
            if form['password_ch'].value() == form['password_ch_new'].value():
                password = form['password_ch'].value()
                user.set_password(password)
                user.save()
                return redirect('details_list')
            else:
                args['error'] = 'Пароли не совпадают!'
    form = UserFormChangePassword()
    args['form'] = form
    address[user.username] = '/user/' + user.username + '/'
    address_list.append(user.username)
    address['Новый пароль'] = request.get_full_path()
    address_list.append('Новый пароль')
    args['address'] = address
    args['address_list'] = address_list
    return render(request, 'change_password.html', args)


""""*************************************** Изменеие профиля пользователя *******************************************"""


@login_required
def user_edit(request):
    args = {}
    address = {}
    address_list = []
    user = request.user
    if request.method == "POST":
        form = UserFormEdit(request.POST, request.FILES)
        profile_form = ProfileFormEdit(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid() and profile_form.is_valid():
            email = User.objects.filter(email=form.cleaned_data['email']).exists()
            if email and user.email != form.cleaned_data['email']:
                args['error'] = 'Пользователь с таким email уже существует!'
            else:
                user.first_name = form['first_name'].value()
                user.last_name = form['last_name'].value()
                user.email = form['email'].value()
                user.save()
                profile_form.save()
                return HttpResponseRedirect('/user/')

    else:
        form = UserFormEdit(instance=request.user)
        profile_form = ProfileFormEdit(instance=request.user.profile)
    args['form'] = form
    args['profile_form'] = profile_form
    args['user_image'] = user.profile.image
    address[user.username] = '/user/' + user.username + '/'
    address_list.append(user.username)
    address['Редактирование профиля'] = request.get_full_path()
    address_list.append('Редактирование профиля')
    args['address'] = address
    args['address_list'] = address_list
    return render(request, 'user_profile_edit.html', args)


""""******************************************* Публикация товара ***************************************************"""


@user_passes_test(lambda u: u.is_superuser)
def publicate_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    item.publicate_item()
    category = Category.objects.get(id=item.category_id)
    category.item_count = Item.objects.all().filter(category_id=item.category_id, publicate=True).count()
    category.save(update_fields=['item_count'])
    return redirect('goods_list')


""""********************************************* Скрытие товара ****************************************************"""


@user_passes_test(lambda u: u.is_superuser)
def unpublicate_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    item.unpublicate_item()
    category = Category.objects.get(id=item.category_id)
    category.item_count = Item.objects.all().filter(category_id=item.category_id, publicate=True).count()
    category.save(update_fields=['item_count'])
    return redirect('goods_list')


""""************************************* Все комментарии пользователя **********************************************"""


@login_required()
def user_comments(request, username):
    args = {}
    address = {}
    address_list = []
    user = User.objects.get(username=username)
    comments = user.author_comments.all().values('author__username', 'id', 'author__profile__image', 'item__id',
                                                  'item__category__title', 'item__title', 'created_date', 'text',
                                                  'author__id').order_by('created_date').reverse()
    args['comments'] = comments
    address[user.username] = '/user/' + user.username + '/'
    address_list.append(user.username)
    address['Комментария пользователя'] = request.get_full_path()
    address_list.append('Комментария пользователя')
    args['address'] = address
    args['address_list'] = address_list
    return render(request, 'user_comments.html', args)