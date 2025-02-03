from apps.activities import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'language', 'updated_at')
    readonly_fields = ('created_at', 'updated_at', 'slug')


@admin.register(models.SiteVisit)
class SiteVisitAdmin(admin.ModelAdmin):
    list_display = ('name', 'language', 'updated_at')
    readonly_fields = ('created_at', 'updated_at', 'slug')