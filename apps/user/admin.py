from django.contrib import admin
from django.contrib.auth.models import User
# Register your models here.
from.models import UserProfile , EmailVerifyCode

from django.contrib.auth.admin import UserAdmin
# 取消注册
admin.site.unregister(User)


class UserProfileType(admin.StackedInline):
    model = UserProfile


class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileType]


admin.site.register(User, UserProfileAdmin)


@admin.register(EmailVerifyCode)
class EmailVerifeCodeAdmin(admin.ModelAdmin):

    list_display =  ('code',)