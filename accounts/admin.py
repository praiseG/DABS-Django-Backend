from django.contrib import admin

# Register your models here.
from .models import MyUser


class MyUserAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'designation',
        'role',
        'created_at',
        'last_login',
        'is_staff',
        'is_superuser',
        'is_active',
    )
admin.site.register(MyUser, MyUserAdmin)