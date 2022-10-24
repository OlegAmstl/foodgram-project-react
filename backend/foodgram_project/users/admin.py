from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import SubscribeUser, MyUser


class SubscribeUserAdmin(admin.ModelAdmin):
    '''Класс SubscribeUserAdmin.'''

    list_display = (
        'pk',
        'user',
        'author',
    )
    list_editable = (
        'user',
        'author',
    )
    search_fields = ('user__username', 'author__username')


class MyUserAdmin(UserAdmin):
    list_filter = ('username', 'email')


admin.site.register(MyUser, MyUserAdmin)
admin.site.register(SubscribeUser, SubscribeUserAdmin)
