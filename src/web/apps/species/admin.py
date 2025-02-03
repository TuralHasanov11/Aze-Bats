from apps.species import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class BatImageInlineAdmin(admin.StackedInline):
    model = models.BatImage


class BatAttributeInlineAdmin(admin.StackedInline):
    model = models.BatAttribute


@admin.register(models.Bat)
class BatAdmin(admin.ModelAdmin):
    list_display = ("name", "is_in_red_list", "genus", "updated_at")
    inlines = [BatImageInlineAdmin, BatAttributeInlineAdmin]
    readonly_fields = ("created_at", "updated_at", "slug")


@admin.register(models.Genus)
class GenusModel(admin.ModelAdmin):
    list_display = ("name", "family", "updated_at")
    readonly_fields = ("created_at", "updated_at", "slug")


@admin.register(models.Family)
class FamilyModel(admin.ModelAdmin):
    list_display = ("name", "updated_at")
    readonly_fields = ("created_at", "updated_at", "slug")