from django.urls import path
from . import views

urlpatterns = [
    #l login_required
    path('not_login', views.not_login),
    # Common
    path('uploadImage', views.uploadImage),
    path('removeImage', views.removeImage),
    path('uploadImg_markdown', views.uploadImg_markdown),
    path('removeImg_markdown', views.removeImg_markdown),
    path('getBriefWallList', views.getBriefWallList),
    # Auth
    path('getPermissionGroupMembers', views.getPermissionGroupMembers),
    path('register', views.register),
    path('registerWX', views.registerWX),
    path('login', views.loginView),
    path('loginWX', views.loginWX),
    path('logout',views.logoutView),
    path('checkBoundEMail', views.checkBoundEMail),
    path('getUserBaseInfo', views.getUserBaseInfo),
    path('getUserProfile', views.getUserProfile),
    path('getCaptcha', views.getCaptcha),
    path('getSMSCaptcha', views.getSMSCaptcha),
    path('searchUser', views.searchUser),
    path('updateUser', views.updateUser),
    path('changePassword', views.changePassword),
    path('findpassword', views.findpassword),
    path('getMessage', views.getMessage),
    path('bindWX', views.bindWX),
    path('uploadAvatar', views.uploadAvatar),
    path('follow', views.follow),
    path('unFollow', views.unFollow),
    # Activity
    path('signUp', views.signUp),
    path('canSign_JinGui', views.canSign_JinGui),
    path('IsFirstSignToday_JinGui', views.IsFirstSignToday_JinGui),
    path('sign_JinGui', views.sign_JinGui),
    path('getStatistics_JinGui', views.getStatistics_JinGui),
    path('getStatistics_JinGui_unsign', views.getStatistics_JinGui_unsign),
    path('getSignStatus', views.getSignStatus),
    path('uploadImg_JinGui', views.uploadImg_JinGui),
    path('removeImg_JinGui', views.removeImg_JinGui),
    path('uploadAudio_JinGui', views.uploadAudio_JinGui),
    path('detail_JinGui', views.detail_JinGui),
    # Admin - User
    path('getUserList', views.getUserList),
    path('getUserDetail', views.getUserDetail),
    path('updateUserAdmin', views.updateUserAdmin),
    path('deleteUser', views.deleteUser),
    # Admin - Bank
    path('getBankChapters', views.getBankChapters),
    path('getBankUploadHistory', views.getBankUploadHistory),
    path('uploadBank', views.uploadBank),
    # Admin - File
    path('getFileUploadHistory', views.getFileUploadHistory),
    path('uploadFile', views.uploadFile),
    # Love
    path('searchLoveItem', views.searchLoveItem),
    path('getLoveList', views.getLoveList),
    path('getLoveDetail', views.getLoveDetail),
    path('thumbsUpLove', views.thumbsUpLove),
    path('submitLove', views.submitLove),
    path('removeLove', views.removeLove),
    path('submitLoveComment', views.submitLoveComment),
    # Lose
    path('searchLoseItem', views.searchLoseItem),
    path('getLoseList', views.getLoseList),
    path('getLoseDetail', views.getLoseDetail),
    path('submitLose', views.submitLose),
    path('removeLose', views.removeLose),
    path('submitLoseComment', views.submitLoseComment),
    # Deal
    path('searchDealItem', views.searchDealItem),
    path('getDealList', views.getDealList),
    path('getDealDetail', views.getDealDetail),
    path('submitDeal', views.submitDeal),
    path('submitDealComment', views.submitDealComment),
    path('removeDeal', views.removeDeal),
    path('dealChange', views.dealChange),
    # Help
    path('submitHelp', views.submitHelp),
    path('getHelpList', views.getHelpList),
    path('getHelpDetail', views.getHelpDetail),
    path('submitHelpComment', views.submitHelpComment),
    path('removeHelp', views.removeHelp),
    # Article
    path('searchArticle', views.searchArticle),
    path('searchArticleByUser', views.searchArticleByUser),
    path('searchArticleByTag', views.searchArticleByTag),
    path('getBriefArticleList', views.getBriefArticleList),
    path('getArticleList', views.getArticleList),
    path('getArticleDetail', views.getArticleDetail),
    path('submitArticle', views.submitArticle),
    path('removeArticle', views.removeArticle),
    path('thumbsUpArticle', views.thumbsUpArticle),
    path('submitArticleComment', views.submitArticleComment),
    path('addArticleViewCount', views.addArticleViewCount),
    # Bank
    path('getBankUpdateMessage', views.getBankUpdateMessage),
    path('getBankSubjects', views.getBankSubjects),
    path('getNumQuestion', views.getNumQuestion),
    path('submitBank', views.submitBank),
    path('handExam', views.handExam),
    path('saveBankResult', views.saveBankResult),
    path('getBankResult', views.getBankResult),
    path('removeBankResult', views.removeBankResult),
    path('clearBankResult', views.clearBankResult),
    path('getBriefBankStatistics', views.getBriefBankStatistics),
    path('getBankStatistics', views.getBankStatistics),
    path('addErrorBook', views.addErrorBook),
    path('removeErrorBook', views.removeErrorBook),
    path('clearErrorBook', views.clearErrorBook),
    path('searchQuestion', views.searchQuestion),
    path('getErrorBook', views.getErrorBook),
    # File
    path('getFileSubjects', views.getFileSubjects),
    path('getFileList', views.getFileList),
    path('addFileViewCount', views.addFileViewCount),
    path('addFileDownloadCount', views.addFileDownloadCount),
    # Club
    # path('getClubDetail', views.getClubDetail),
    # Medicine
    path('getAllMedicine_Type', views.getAllMedicine_Type),
    path('getAllMedicine_Flavor', views.getAllMedicine_Flavor),
    path('getAllMedicine_Channel', views.getAllMedicine_Channel),
    path('getMedicineDetail', views.getMedicineDetail),
    path('searchMedicine', views.searchMedicine),
    path('autoComplete_searchMedicine', views.autoComplete_searchMedicine),
    # Prescription
    path('getAllPrescription', views.getAllPrescription),
    path('getPrescriptionDetail', views.getPrescriptionDetail),
    path('searchPrescription', views.searchPrescription),
    path('autoComplete_searchPrescription', views.autoComplete_searchPrescription),
    # Acupoint
    path('getAllAcupoint_Channel', views.getAllAcupoint_Channel),
    path('getAllAcupoint_Type', views.getAllAcupoint_Type),
    path('getAcupointDetail', views.getAcupointDetail),
    path('searchAcupoint', views.searchAcupoint),
    path('autoComplete_searchAcupoint', views.autoComplete_searchAcupoint),
    # Virtual Diagnosis
    path('addNewLog_VirtualDiagnosis', views.addNewLog_VirtualDiagnosis),
    path('getLog_VirtualDiagnosis', views.getLog_VirtualDiagnosis),
    path('getLogDetail_VirtualDiagnosis', views.getLogDetail_VirtualDiagnosis),
    # Hot
    path('getBriefHotList', views.getBriefHotList),
    path('getHotList', views.getHotList),
    path('getHotDetail', views.getHotDetail),
    path('addHot', views.addHot),
    path('deleteHot', views.deleteHot),
    # Lecture
    path('getBriefLectureList', views.getBriefLectureList),
    path('getLectureList', views.getLectureList),
    path('getLectureDetail', views.getLectureDetail),
    path('addLecture', views.addLecture),
    path('deleteLecture', views.deleteLecture),
]
