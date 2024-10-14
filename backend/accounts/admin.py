from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, VisitorActivityLog


class CustomUserAdmin(BaseUserAdmin):
    # Configuration des champs à afficher dans l'interface d'administration
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    # Champs à éditer dans l'administration (création et modification)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login',)}),
    )

    # Configuration pour la création d'un nouvel utilisateur dans l'administration
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'is_staff', 'is_superuser'),
        }),
    )

    filter_horizontal = ('groups', 'user_permissions')


# Enregistrement du modèle CustomUser avec l'admin personnalisée
admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(VisitorActivityLog)
class VisitorActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp', 'ip_address', 'location')
    search_fields = ( 'action', 'ip_address', 'location')
    list_filter = ('action', 'timestamp', 'location')

