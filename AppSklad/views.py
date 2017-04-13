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
import json


"""**************************************** Отображение списка деталей **********************************************"""


def details_list(request, page_number=1):
    args = {}
    args.update(csrf(request))
    sum_price = 0
    if request.user.is_authenticated():
        request.user.profile.last_seen = timezone.now()
        request.user.profile.save(update_fields=['last_seen'])
    if request.GET and len(request.GET.get('title')) > 0:
        newuser_form = SearchForm(request.GET)
        all_details = Detail.objects.filter(title__contains=request.GET.get('title')).select_related('color').order_by('category__title', 'title')
        for i in all_details:
            sum_price += i.price * i.count
        args['form'] = newuser_form
        args['new_details'] = all_details
        args['pg'] = False
    else:
        all_details = Detail.objects.all().select_related('color').order_by('category__title', 'title')
        for i in all_details:
            sum_price += i.price * i.count
        current_page = Paginator(all_details, 10)
        args['new_details'] = current_page.page(page_number)
        count = all_details.count()
        args['pg'] = True
        args['count'] = count
    args['sum'] = sum_price
    return render(request, 'sklad/details_list.html', args)


"""**************************************** Отображение списка товаров **********************************************"""


def available_goods(item_details):         # функция расчёта количества доступных товаров
    dict = {}
    max = 0
    details = Detail.objects.all()
    for detail in details:
        dict[detail.title] = detail.count
        if detail.count > max:
            max = detail.count
    minim = max
    for detail in item_details:
        current = dict[detail.detail.title] // detail.detail_count
        if current < minim:
            minim = current
    return minim


def goods_list(request, category_value=None):
    args = {}
    if request.GET and request.GET.get('title').count() > 0:
        new_form = SearchForm(request.GET)
        if category_value is None:
            all_items = Item.objects.all().select_related('category').filter(publicate=True, title__contains=request.GET.get('title')).order_by("title")
        else:
            all_items = Item.objects.all().select_related('category').filter(publicate=True, category__title_plural=category_value, title__contains=request.GET.get('title')).order_by(
                "title")
            args['category_value'] = category_value
        if category_value is None:
            publiched_items = Item.objects.all().select_related('category').filter(publicate=False, title__contains=request.GET.get('title')).order_by("category", "title")
            count = publiched_items.count()
            args['publiched_items'] = publiched_items
            args['count'] = count
        categories = Category.objects.all()

        # получение данных о количестве товаров в каждой категории
        for category in categories:
            category.item_count = all_items.filter(category=category).distinct().count()
            category.save(update_fields=['item_count'])

        categories = [x for x in categories if x.item_count != 0]
        args['form'] = new_form
        args['search'] = True
        args['categories'] = categories
    else:
        if category_value is None:
            all_items = Item.objects.all().select_related('category').filter(publicate=True).order_by("title")
        else:
            all_items = Item.objects.all().select_related('category').filter(publicate=True, category__title_plural=category_value).order_by("title")
            args['category_value'] = category_value
        if category_value is None:
            publiched_items = Item.objects.all().select_related('category').filter(publicate=False).order_by("category", "title")
            count = publiched_items.count()
            args['publiched_items'] = publiched_items
            args['count'] = count
        categories = Category.objects.all()

        # получение данных о количестве товаров в каждой категории
        for category in categories:
            category.item_count = all_items.filter(category=category).distinct().count()
            category.save(update_fields=['item_count'])

        # расчёт затрат, прибыли товаров, а также расчёт количества доступных товаров
        for item in all_items:
            expenses = 0
            item_details = ItemDetails.objects.select_related('detail').filter(item=item)  # получение деталей, использованных для данного товара

            # расчёт затрат данного товара
            for detail in item_details:
                expenses += detail.detail.price * detail.detail_count
            item.available = available_goods(item_details)
            item.expenses = expenses
            item.profit = item.price - expenses
            item.save(update_fields=['available', 'expenses', 'profit'])
        args['categories'] = categories
        args['search'] = False
    args['all_items'] = all_items
    if category_value is None:
        return render(request, 'sklad/goods_list.html', args)
    else:
        return render(request, 'sklad/category_list.html', args)


"""**************************************** Отображение списка товаров пользователя**********************************"""


def user_items(request, username):
    args = {}
    user = User.objects.get(username=username)
    all_items = Item.objects.all().filter(publicate=True, author=user).order_by("title")
    if user.is_superuser:
        publiched_items = Item.objects.all().filter(publicate=False).order_by("category", "title")
    else:
        publiched_items = Item.objects.all().filter(publicate=False, author=user).order_by("category", "title")
    count = publiched_items.count()
    categories = Category.objects.all()

    # получение данных о количестве товаров в каждой категории
    for category in categories:
        category.item_count = all_items.filter(category=category).distinct().count()
        category.save(update_fields=['item_count'])

    # расчёт затрат, прибыли товаров, а также расчёт количества доступных товаров
    for item in all_items:
        expenses = 0
        item_details = ItemDetails.objects.filter(item=item)  # получение деталей, использованных для данного товара

        # расчёт затрат данного товара
        for detail in item_details:
            expenses += detail.detail.price * detail.detail_count
        item.available = available_goods(item_details)
        item.expenses = expenses
        item.profit = item.price - expenses
        item.save(update_fields=['available', 'expenses', 'profit'])
    args['all_items'] = all_items
    args['publiched_items'] = publiched_items
    args['count'] = count
    args['categories'] = categories
    args['user_object'] = user
    return render(request, 'sklad/user_items.html', args)


"""**************************************** Расчёт максимальной прибыли *********************************************"""


def available_goods2(all_items, dict_details):
    sum_min = 0
    for i in range(len(all_items)):
        item_details = ItemDetails.objects.filter(item=all_items[i])
        min = 15000
        for detail in item_details:
            current = dict_details[detail.detail.pk] // detail.detail_count
            if current < min:
                if current < 0:
                    min = 0
                else:
                    min = current
        sum_min += min
        all_items[i].available = min
    if sum_min == 0:
        return False
    return all_items


def item_profit(request, category=None):
    args = {}
    list_of_items = []
    sum_profit = 0

    # проверка на тип расчёта максимальной прибыли
    if category:
        all_items = list(Item.objects.filter(category__title_plural=category, publicate=True).order_by("title"))  # набор всех товаров
        details = list(Detail.objects.filter(category__title_plural=category).order_by("title"))  # набор всех деталей
        args['category'] = category
    else:
        all_items = list(Item.objects.filter(publicate=True).order_by("title"))  # набор всех товаров
        details = list(Detail.objects.all().order_by("title"))  # набор всех деталей
    dict_details = {detail.pk: detail.count for detail in details}  # словать деталей
    while True:

        max_profit = 0
        max_profit_item = None

        # поиск самого выгодного товара
        all_items = available_goods2(all_items, dict_details)
        if not all_items:
            break
        for item in all_items:
            prof = item.available*item.profit
            if prof > max_profit:
                max_profit = prof
                max_profit_item = item  # сохранение объекта самого выгодного товара
            if max_profit_item is None:
                break

        if max_profit_item is None:
            break

        max_profit_item_details = ItemDetails.objects.filter(item=max_profit_item)  # набор деталей выбранного товара

        # вычисление остатка деталей, после происзводства доступного количества данного товара
        for detail in max_profit_item_details:
            dict_details[detail.detail.pk] -= detail.detail_count*max_profit_item.available

        # удаление товара
        all_items.remove(max_profit_item)
        max_profit_item.count = max_profit_item.available
        max_profit_item.received = (max_profit_item.available * max_profit_item.profit) +\
                                   (max_profit_item.available * max_profit_item.expenses)
        max_profit_item.profit = max_profit_item.available * max_profit_item.profit
        max_profit_item.expenses = max_profit_item.available * max_profit_item.expenses
        list_of_items.append(max_profit_item)
        sum_profit += max_profit_item.profit

        # проверка на количество оставшихся деталей
        if len(all_items) == 0:
            break
    for detail in details:
        detail.count = dict_details[detail.pk]
    args['list_of_items'] = list_of_items
    args['details'] = details
    args['sum_profit'] = sum_profit
    args['dict_details'] = dict_details
    return render(request, 'sklad/goods_profit.html', args)


"""*************************************** Детальная информация о товаре *******************************************"""


def item_detail(request, pk):
    args = {}
    item = get_object_or_404(Item, pk=pk)
    category_items = list(Item.objects.filter(category__title=item.category.title).order_by('category__title', 'title'))
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
            return redirect('AppSklad.views.item_detail', pk=item.pk)
    else:
        form = CommentFormEdit()
    args['form'] = form
    args['item'] = item
    return render(request, 'item_detail.html', args)


"""*************************************** Редактирование товара ****************************************************"""


@login_required
def item_edit(request, pk):
    args = {}
    item = get_object_or_404(Item, pk=pk)
    itemDetailsFormSet = inlineformset_factory(Item, ItemDetails, form=ItemDetailsForm, extra=14)
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, instance=item)
        formset = itemDetailsFormSet(request.POST, instance=item)
        if form.is_valid() and formset.is_valid():
            new_form = form.save(commit=False)
            new_form.price = form.cleaned_data['price']
            new_form.category = form.cleaned_data['category']
            new_form.title = form.cleaned_data['title']
            new_form.author = auth.get_user(request)
            new_form.save()
            formset.save()
            return redirect('AppSklad.views.item_detail', pk=item.pk)
        else:
            form = ItemForm(instance=item)
            formset = itemDetailsFormSet(instance=item)
    else:
        formset = itemDetailsFormSet(instance=item)
        form = ItemForm(instance=item)
    args['formset'] = formset
    args['form'] = form
    args['item_image'] = item.image
    return render(request, 'item_edit.html', args)


"""********************************************* Удаление товара ****************************************************"""


@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    item.delete()
    return redirect('AppSklad.views.goods_list')


"""********************************************* Создание товара ****************************************************"""


@login_required
def item_new(request, category=None):
    args = {}
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.author = auth.get_user(request)
            new_form.save()
            return redirect("AppSklad.views.item_edit", pk=new_form.pk)
        else:
            form = ItemForm(request.POST)
    else:

        form = ItemForm()
    args['form'] = form
    if category:
        args['category'] = category
    return render(request, 'item_edit.html', args)


"""************************************** Детальная информация о детали *********************************************"""


def details_detail(request, pk):
    args = {}
    detail = get_object_or_404(Detail, pk=pk)
    args['detail'] = detail
    return render(request, 'details_detail.html', args)


"""*************************************** Редактирование детали ****************************************************"""


@login_required
def detail_edit(request, pk=1):
    args = {}
    detail = get_object_or_404(Detail, pk=pk)
    if request.method == "POST":
        form = DetailForm(request.POST, request.FILES, instance=detail)
        if form.is_valid():
            detail = form.save(commit=False)
            detail.save()
            return redirect('AppSklad.views.details_detail', pk=detail.pk)
    else:
        form = DetailForm(instance=detail)
    args['form'] = form
    args['detail_image'] = detail.image
    return render(request, 'detail_edit.html', args)


"""*************************************** Создание новой детали ****************************************************"""


@login_required
def detail_new(request):
    args = {}
    new = True
    if request.method == "POST":
        form = DetailForm(request.POST, request.FILES)
        if form.is_valid():
            detail = form.save(commit=False)
            detail.save()
            return redirect('AppSklad.views.details_detail', pk=detail.pk)
    else:
        form = DetailForm()
    args['form'] = form
    args['new'] = new
    return render(request, 'detail_edit.html', args)


"""********************************************* Удаление детали ****************************************************"""


@login_required
def detail_delete(request, pk):
    detail = get_object_or_404(Detail, pk=pk)
    detail.delete()
    return redirect('AppSklad.views.details_list')


""""************************************** Создание новой категории *************************************************"""


@login_required
def category_new(request):
    args = {}
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return redirect('AppSklad.views.goods_list')
    else:
        form = CategoryForm()
    args['form'] = form
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
    # return HttpResponse(json.dumps({'ok': ok}), content_type="application/json")
    return HttpResponse("ok")


""""****************************************** Профиль пользователя *************************************************"""


@login_required
def user_profile(request, username):
    args = {}
    user = User.objects.get(username=username)
    user_form = UserForm(instance=user)
    profile_user = ProfileForm(instance=user.profile)
    admin = user.is_superuser
    args['admin'] = admin
    args['user_form'] = user_form
    args['user_object'] = user
    args['profile_user'] = profile_user
    return render(request, 'user_profile.html', args)


""""********************************************** Смена ппароля ****************************************************"""


@login_required
def change_password(request):
    args = {}
    if request.method == "POST":
        user = request.user
        form = UserFormChangePassword(request.POST)
        if form.is_valid():
            if form['password_ch'].value() == form['password_ch_new'].value():
                password = form['password_ch'].value()
                user.set_password(password)
                user.save()
                return redirect('AppSklad.views.details_list')
            else:
                args['error'] = 'Пароли не совпадают.'
    form = UserFormChangePassword()
    args['form'] = form
    return render(request, 'change_password.html', args)


""""*************************************** Изменеие профиля пользователя *******************************************"""


@login_required
def user_edit(request):
    args = {}
    user = request.user
    if request.method == "POST":
        form = UserFormEdit(request.POST, request.FILES)
        profile_form = ProfileFormEdit(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid() and profile_form.is_valid():
            user.first_name = form['first_name'].value()
            user.last_name = form['last_name'].value()
            user.email = form['email'].value()
            user.save()
            profile_form.save()
            return HttpResponseRedirect('/user/')
    form = UserFormEdit(instance=request.user)
    profile_form = ProfileFormEdit(instance=request.user.profile)
    args['form'] = form
    args['profile_form'] = profile_form
    args['user_image'] = user.profile.image
    return render(request, 'user_profile_edit.html', args)


""""******************************************* Публикация товара ***************************************************"""


@user_passes_test(lambda u: u.is_superuser)
def publicate_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    item.publicate_item()
    return redirect('AppSklad.views.goods_list')


""""********************************************* Скрытие товара ****************************************************"""


@user_passes_test(lambda u: u.is_superuser)
def unpublicate_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    item.unpublicate_item()
    return redirect('AppSklad.views.goods_list')


""""************************************* Все комментарии пользователя **********************************************"""


@login_required()
def user_comments(request, username):
    args = {}
    userr = User.objects.get(username=username)
    comments = userr.comments.all().order_by('created_date').reverse()
    args['comments'] = comments
    return render(request, 'user_comments.html', args)