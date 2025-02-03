from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from tinymce.widgets import TinyMCE
from django.db import models

from apps.species.models import Bat, BatAttribute, BatImage, Family, Genus


class BatImageInlineAdmin(admin.StackedInline):
    model = BatImage


class BatAttributeInlineAdmin(admin.StackedInline):
    model = BatAttribute


@admin.register(Bat)
class BatAdmin(admin.ModelAdmin):
    list_display = ("name", "is_in_red_list", "genus", "updated_at")
    inlines = [BatImageInlineAdmin, BatAttributeInlineAdmin]
    readonly_fields = ("created_at", "updated_at", "slug")


@admin.register(Genus)
class GenusModel(admin.ModelAdmin):
    list_display = ("name", "family", "updated_at")
    readonly_fields = ("created_at", "updated_at", "slug")


@admin.register(Family)
class FamilyModel(admin.ModelAdmin):
    list_display = ("name", "updated_at")
    readonly_fields = ("created_at", "updated_at", "slug")
    formfield_overrides = {models.TextField: {"widget": TinyMCE()}}
