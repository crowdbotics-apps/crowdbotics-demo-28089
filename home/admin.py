from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from home.models import Plan, Subscription, App


class BaseAdmin(admin.ModelAdmin):
    advanced_fieldset = (
        _('Advanced options'), {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at',),
        })


@admin.register(Plan)
class PlanAdmin(BaseAdmin):
    list_display = ('name', 'price', 'is_active')
    search_fields = ('name',)
    fieldsets = (
        (None, {
            'fields': list_display
        }),
        BaseAdmin.advanced_fieldset
    )


@admin.register(Subscription)
class SubscriptionAdmin(BaseAdmin):
    list_display = ('plan', 'app', 'is_active')
    search_fields = ('plan__name', 'app__name')
    list_filter = ('plan__name', 'is_active')
    fieldsets = (
        (None, {
            'fields': list_display
        }),
        BaseAdmin.advanced_fieldset
    )


@admin.register(App)
class AppAdmin(BaseAdmin):
    list_display = ('name', 'type', 'framework', 'domain_name', 'user',
                    'is_active')
    search_fields = ('name',)
    list_filter = ('framework', 'type', 'is_active')
    fieldsets = (
        (None, {
            'fields': list_display
        }),
        BaseAdmin.advanced_fieldset
    )
