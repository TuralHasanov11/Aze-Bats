from apps.activities import models
from django.contrib import admin


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'language', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')


@admin.register(models.SiteVisit)
class SiteVisitAdmin(admin.ModelAdmin):
    list_display = ('name', 'language', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')