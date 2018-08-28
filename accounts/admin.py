from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
from .models import MyUser
from .forms import (
    UserAdminCreationForm, UserAdminChangeForm
)


class MyUserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

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

    list_filter = ('is_active','is_staff','is_superuser'
                )

    search_fields = ('email', 'name')
    ordering = ('email', 'name')
    filter_horizontal = ()
    fieldsets = (
            (None, {'fields': ('email', 'password')}),
            ('Personal Info', {'fields': ('name', 'designation')}),
            ('Permissions', {'fields': ('role', 'is_staff', 'is_superuser', 'is_active')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'password1', 'password2')}),
        ('Personal Info', {'classes': ('wide',), 'fields': ('name', 'designation')}),
        ('Permissions', {'classes': ('wide',), 'fields': ('role', 'is_staff', 'is_superuser', 'is_active')}),
    )

admin.site.register(MyUser, MyUserAdmin)
admin.site.unregister(Group)