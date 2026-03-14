from django.contrib import admin
from django.contrib.auth.hashers import make_password
from app.models import AdminAccounts
from .models import Users, UserToken

"""
AdminAccounts.objects.get_or_create(
    username="delarosa",
    defaults={
        "password_hash": make_password("capsword"),
        "role": "admin"
    }
)
"""


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name')

@admin.register(UserToken)
class UserTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')




