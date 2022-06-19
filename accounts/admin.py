from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.forms import CustomUserChangeForm
from accounts.forms import CustomUserCreationForm
from accounts.models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'premium', 'is_staff', ]
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('premium',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('premium',)}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
