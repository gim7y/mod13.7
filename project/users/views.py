from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import RegisterUserForm, LoginUserForm, OneTimeCodeForm, NewUserChangeForm
from .models import OneTimeCode

import random

# Create your views here.

class BaseRegisterView(CreateView):
    model = User
    form_class = RegisterUserForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('/')

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        pasw = form.cleaned_data.get('password1')
        email = form.cleaned_data.get('email')
        user = authenticate(username=username, password=pasw)
        OneTimeCode.objects.filter(user=user).delete()
        code = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyzCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(6))
        OneTimeCode.objects.create(code=code, user=user)
        code = OneTimeCode.objects.get(user=user)
        print(user.email)
        send_mail("Сообщение",
                  "Имя пользователя:{}, пароль:{}".format(user.username, code.code),
                  from_email='g1.f4g@yandex.ru',
                  recipient_list=[email],
                  fail_silently=False)
        return redirect('users:log_next')

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'


def view_code(request):
    form = OneTimeCodeForm()
    return render(request, 'users/log_next.html', {'form': form, 'title': 'Код проверки', })


def log_with_code_view(request):
    username = request.POST['username']
    code = request.POST['code']
    user = User.objects.get(username=username)
    email = User.objects.get(email=user.email)
    if OneTimeCode.objects.filter(code=code, user=user).exists():
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        OneTimeCode.objects.filter(user=user).delete()
        return render(request, 'users/sign_success.html', {'success login': 'Вы будете перенаправлены на страницу ЛК', })
    else:
        return render(request, 'users/signup.html', {'error': 'ошибка ввода имени или пароля', })
    return redirect('users:login')
