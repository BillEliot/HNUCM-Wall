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
    path('getLoseList', views.getLoseList),
    path('getDealList', views.getDealList),
    path('getArticleList', views.getArticleList),
    path('getLoveDetail', views.getLoveDetail),
    path('getLoseDetail', views.getLoseDetail),
    path('getDealDetail', views.getDealDetail),
    path('thumbsUp', views.thumbsUp),
    path('getNumQuestion', views.getNumQuestion),
    # Upload
    path('uploadLoveImg', views.uploadLoveImg),
    path('removeLoveImg', views.removeLoveImg),
    path('uploadLoseImg', views.uploadLoseImg),
    path('removeLoseImg', views.removeLoseImg),
    path('uploadDealImg', views.uploadDealImg),
    path('removeDealImg', views.removeDealImg),
    # Submit
    path('submitLove', views.submitLove),
    path('submitLose', views.submitLose),
    path('submitDeal', views.submitDeal),
    path('submitBank', views.submitBank),
    path('submitLoveComment', views.submitLoveComment),
    path('submitLoseComment', views.submitLoseComment),
    path('submitUserComment', views.submitUserComment),
    path('submitDealComment', views.submitDealComment),
    path('submitArticle', views.submitArticle)
]
