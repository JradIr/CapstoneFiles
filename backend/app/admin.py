from django.contrib import admin
from django.contrib.auth.hashers import make_password
from app.models import AdminAccounts

AdminAccounts.objects.get_or_create(
    username="delarosa",
    defaults={
        "password_hash": make_password("capsword"),
        "role": "admin"
    }
)



