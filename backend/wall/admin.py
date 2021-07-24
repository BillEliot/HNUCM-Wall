from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from wall.models import *

admin.site.site_title = u'湖南中医药大学墙墙 管理页面'
admin.site.site_header = u'湖南中医药大学墙墙 管理页面'

'''
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'bio', 'gender', 'email', '_class', 'coin')
    list_filter=('gender', '_class')
    search_fields = ('id', 'username','email')
'''

class BankAdmin(admin.ModelAdmin):
    list_display = ('title', 'questionType', 'chapter')
    list_filter=('questionType', 'chapter')
    search_fields = ('title',)

class LoveAdmin(admin.ModelAdmin):
    filter_horizontal = ('userTo', 'thumbsUpUser',)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'tags', 'publicDate', 'editDate', 'isAdopted')
    list_editable = ('isAdopted',)
    list_filter=('tags', 'isAdopted')
    search_fields = ('title',)

class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', '_type', 'subType')
    search_fields = ('name',)

class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('name', '_type')
    filter_horizontal = ('medicine',)

admin.site.register(User, UserAdmin)
admin.site.register(Bank, BankAdmin)
admin.site.register(Love, LoveAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Bank_UpdateMessage)
admin.site.register(Bank_Chapter)
admin.site.register(Bank_Subject)
admin.site.register(CommonFile)
admin.site.register(File)
admin.site.register(File_Subject)
#admin.site.register(Activity_JinGui)
admin.site.register(Medicine, MedicineAdmin)
admin.site.register(Prescription, PrescriptionAdmin)
admin.site.register(Match)
admin.site.register(Banner)
