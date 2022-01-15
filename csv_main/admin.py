from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


class Admin(UserAdmin):
    model = User
    list_display = ['email', 'username', ]


