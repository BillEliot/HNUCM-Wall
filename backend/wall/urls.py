from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('register', views.register),
    path('login', views.login),
    path('logout',views.logout),
    path('getUserBaseInfo', views.getUserBaseInfo),
    path('getCaptcha', views.getCaptcha),
    # Query
    path('searchUser', views.searchUser),
    path('getUserProfile', views.getUserProfile),
    path('getLoveList', views.getLoveList),
    path('thumbsUp', views.thumbsUp),
    # Upload
    path('uploadLoveImg', views.uploadLoveImg),
    path('removeLoveImg', views.removeLoveImg),
    # Create
    path('submitLove', views.submitLove)
]
