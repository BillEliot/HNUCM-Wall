from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('register', views.register),
    path('registerWX', views.registerWX),
    path('login', views.login),
    path('loginWX', views.loginWX),
    path('logout',views.logout),
    path('checkUniqueEmail', views.checkUniqueEmail),
    path('getUserBaseInfo', views.getUserBaseInfo),
    path('getUserProfile', views.getUserProfile),
    path('getCaptcha', views.getCaptcha),
    path('searchUser', views.searchUser),
    path('submitUserComment', views.submitUserComment),
    path('updateUser', views.updateUser),
    path('changePassword', views.changePassword),
    path('getMessage', views.getMessage),
    path('bindWX', views.bindWX),
    path('uploadAvatar', views.uploadAvatar),
    # Admin - User
    path('getUserList', views.getUserList),
    path('getUserDetail', views.getUserDetail),
    path('updateUserAdmin', views.updateUserAdmin),
    path('deleteUser', views.deleteUser),
    # Love
    path('searchLoveItem', views.searchLoveItem),
    path('getLoveList', views.getLoveList),
    path('getLoveDetail', views.getLoveDetail),
    path('uploadLoveImg', views.uploadLoveImg),
    path('removeLoveImg', views.removeLoveImg),
    path('thumbsUpLove', views.thumbsUpLove),
    path('submitLove', views.submitLove),
    path('submitLoveComment', views.submitLoveComment),
    # Lose
    path('searchLoseItem', views.searchLoseItem),
    path('getLoseList', views.getLoseList),
    path('getLoseDetail', views.getLoseDetail),
    path('uploadLoseImg', views.uploadLoseImg),
    path('removeLoseImg', views.removeLoseImg),
    path('submitLose', views.submitLose),
    path('submitLoseComment', views.submitLoseComment),
    # Deal
    path('searchDealItem', views.searchDealItem),
    path('getDealList', views.getDealList),
    path('getDealDetail', views.getDealDetail),
    path('uploadDealImg', views.uploadDealImg),
    path('removeDealImg', views.removeDealImg),
    path('submitDeal', views.submitDeal),
    path('submitDealComment', views.submitDealComment),
    # Article
    path('searchArticle', views.searchArticle),
    path('searchArticleByUser', views.searchArticleByUser),
    path('searchArticleByTag', views.searchArticleByTag),
    path('getArticleList', views.getArticleList),
    path('getArticleDetail', views.getArticleDetail),
    path('submitArticle', views.submitArticle),
    path('thumbsUpArticle', views.thumbsUpArticle),
    path('submitArticleComment', views.submitArticleComment),
    # Bank
    path('getBankUpdateMessage', views.getBankUpdateMessage),
    path('getBankSubjects', views.getBankSubjects),
    path('getNumQuestion', views.getNumQuestion),
    path('submitBank', views.submitBank),
    path('handExam', views.handExam),
    path('getBankStatistics', views.getBankStatistics),
    path('addErrorBook', views.addErrorBook),
    path('removeErrorBank', views.removeErrorBank),
    # Club
    # path('getClubDetail', views.getClubDetail),
    # Hot
    path('getHotList', views.getHotList),
    path('getHotDetail', views.getHotDetail),
    path('addHot', views.addHot),
    path('deleteHot', views.deleteHot),
    # Lecture
    path('getLectureList', views.getLectureList),
    path('getLectureDetail', views.getLectureDetail),
    path('addLecture', views.addLecture),
    path('deleteLecture', views.deleteLecture),
    # Help
    path('submitHelp', views.submitHelp),
    path('getHelpList', views.getHelpList),
    path('getHelpDetail', views.getHelpDetail),
    path('submitHelpComment', views.submitHelpComment)
]
