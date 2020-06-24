from django.contrib import admin
from wall.models import User, Bank, Article, Bank_UpdateMessage, Bank_Chapter, Bank_Subject

admin.site.site_title = u'湖南中医药大学墙墙 管理页面'
admin.site.site_header = u'湖南中医药大学墙墙 管理页面'

class UserAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'bio', 'gender', 'email', '_class', 'coin')
    list_filter=('gender', '_class')
    search_fields = ('id', 'nickname','email')

class BankAdmin(admin.ModelAdmin):
    list_display = ('title', 'questionType', 'chapter')
    list_filter=('questionType', 'chapter')
    search_fields = ('title',)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'tags', 'publicDate', 'editDate', 'isAdopted')
    list_editable = ('isAdopted',)
    list_filter=('tags', 'isAdopted')
    search_fields = ('title',)

admin.site.register(User, UserAdmin)
admin.site.register(Bank, BankAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Bank_UpdateMessage)
admin.site.register(Bank_Chapter)
admin.site.register(Bank_Subject)
