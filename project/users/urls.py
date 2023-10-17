from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *

app_name = 'users'
urlpatterns = [
    path('login/',
         LoginUser.as_view(), name='login'),
    path('logout/',
         LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('signup/',
         BaseRegisterView.as_view(template_name='users/signup.html'), name='signup'),
    path('next/', view_code, name='log_next'),
    path('next/code/', log_with_code_view, name='view_code')
]
