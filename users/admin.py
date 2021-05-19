from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = (
        'username', 'is_staff', 'is_superuser', 'is_active'
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Permissions'), {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', )
    ordering = ('username', )
    filter_horizontal = ('groups', 'user_permissions',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()  # to disable individual field once

        if not is_superuser:
            disabled_fields |= {'username', 'is_superuser', 'is_admin'}

        for val in disabled_fields:
            if val in form.base_fields:
                form.base_fields[val].disabled = True
        return form


admin.site.register(User, UserAdmin)
