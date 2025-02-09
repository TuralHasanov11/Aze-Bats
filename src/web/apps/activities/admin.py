from apps.activities.models import Project, SiteVisit
from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "language", "updated_at")
    readonly_fields = ("created_at", "updated_at", "slug")
    formfield_overrides = {models.TextField: {"widget": TinyMCE()}}


@admin.register(SiteVisit)
class SiteVisitAdmin(admin.ModelAdmin):
    list_display = ("name", "language", "updated_at")
    readonly_fields = ("created_at", "updated_at", "slug")
    formfield_overrides = {models.TextField: {"widget": TinyMCE()}}
