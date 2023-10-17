from allauth.account.forms import SignupForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms


class EmailVerifyForm(forms.Form):
    code = forms.CharField(max_length=12, label='одноразовый код')


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class NewUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class OneTimeCodeForm(forms.Form):
    username = forms.CharField(max_length=30)
    code = forms.CharField(max_length=30)
