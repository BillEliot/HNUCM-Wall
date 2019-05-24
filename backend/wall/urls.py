from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('register', views.register),
    path('login', views.login),
    path('getUserBaseInfo', views.getUserBaseInfo),
    path('getCaptcha', views.getCaptcha),
    # Query
    path('searchUser', views.searchUser),
    path('getLoveList', views.getLoveList),
    # Upload
    path('uploadLoveImg', views.uploadLoveImg),
    path('removeLoveImg', views.removeLoveImg),
    # Create
    path('submitLove', views.submitLove)
]
