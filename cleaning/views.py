from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, UserLoginForm, OrderForm
from django.contrib.auth.models import AnonymousUser
from .models import *

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            login(request, form.instance)
            return redirect('order_lists')
    else:
        form = UserRegistrationForm()
    return render(request, 'auth/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(login=form.cleaned_data['login'], password=form.cleaned_data['password'])
            print(user)
            if user is not None:
                login(request, user)
                return redirect('order_lists')
            else:
                form.add_error(None, 'Введите правильный логин и пароль. Оба поля могут быть чувствительны к регистру.')
    else:
        form = UserLoginForm()
    return render(request, 'auth/login.html', {'form': form})

def index(request):
    if isinstance(request.user, AnonymousUser):
        data = {
            'orders': 'Здесь пока пустота'
        }
    else:
        user_orders = Order.objects.filter(user_id=request.user)
        data = {
            'orders': user_orders,
        }
    return render(request, "index.html", data)


def create_order(request):
    data = {
        "order_form": OrderForm(),
    }

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.user_id = request.user
            order.save()
            return redirect('order_lists')

    return render(request, 'create_order.html', data)


