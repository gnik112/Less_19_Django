from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserRegister
from .models import *


def index_platform(request):
    content = {
        'title': 'Главная страница',
    }
    return render(request, 'platform.html', content)


def index_games(request):
    # Список игр из БД
    games = Game.objects.all()
    content = {
        'title': 'Магазин',
        'games': games,
    }
    return render(request, 'games.html', content)


def index_cart(request):
    content = {
        'title': 'Корзина',
    }
    return render(request, 'cart.html', content)


# Формирование словаря для шаблона
def info(error, error_show, mess, mess_show):
    return {'error': error, 'error_show': error_show, 'mess': mess, 'mess_show': mess_show}


def sign_up_by_django(request):
    u_info = {}
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = form.cleaned_data['age']
            users = [x.name for x in Buyer.objects.all()]
            if username in users:
                u_info = {'info': info('Пользователь уже существует', True, '', False)}
            else:
                # Добавление пользователя
                Buyer.objects.create(name=username, balance='0.0', age=age)
                u_info = {'info': info('', False, f'Приветствуем, {username}!"', True)}
    else:
        form = UserRegister()
        u_info = {'info': info('Ведите данные для регистрации:', True, '', False)}
    content = u_info
    content['form'] = form
    return render(request, 'registration_page.html', content)


def sign_up_by_html(request):
    if request.method == 'POST':
        # Получение данных
        username = request.POST.get('username')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        age = request.POST.get('age')
        users = [x.name for x in Buyer.objects.all()]
        if username in users:
            content = {'info': info('Пользователь уже существует', True, '', False)}
        else:
            # Добавление пользователя
            Buyer.objects.create(name=username, balance='0.0', age=age)
            content = {'info': info('', False, f'Приветствуем, {username}!"', True)}
    else:
        content = {'info': info('Ведите данные для регистрации:', True, '', False)}
    return render(request, 'registration_page.html', content)


def news(request):
    news_list = News.objects.all().order_by('date')
    paginator = Paginator(news_list, 2)
    page_number = request.GET.get('page')
    news = paginator.get_page(page_number)
    return render(request, 'news.html', {'news': news})
