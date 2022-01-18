from django.contrib import admin
from .models import User, DataScheme, DataSchemeColumn
from django.contrib.auth.admin import UserAdmin


class Admin(UserAdmin):
    model = User
    list_display = ['email', 'username', ]


admin.site.register(DataScheme)
admin.site.register(DataSchemeColumn)
