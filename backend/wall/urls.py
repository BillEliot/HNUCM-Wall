from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('register', views.register),
    path('login', views.login),
    path('logout',views.logout),
    path('getUserBaseInfo', views.getUserBaseInfo),
    path('getUserProfile', views.getUserProfile),
    path('getCaptcha', views.getCaptcha),
    # Query
    path('searchUser', views.searchUser),
    path('getLoveList', views.getLoveList),
    path('getLoveDetail', views.getLoveDetail),
    path('thumbsUp', views.thumbsUp),
    # Upload
    path('uploadLoveImg', views.uploadLoveImg),
    path('removeLoveImg', views.removeLoveImg),
    # Submit
    path('submitLove', views.submitLove),
    path('submitComment', views.submitComment),
    path('submitUserComment', views.submitUserComment)
]
