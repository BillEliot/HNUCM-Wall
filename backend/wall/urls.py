from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('register', views.register),
    path('login', views.login),
    path('getUserBaseInfo', views.getUserBaseInfo),
    path('getCaptcha', views.getCaptcha)
]
