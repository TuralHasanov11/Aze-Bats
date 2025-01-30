from apps.species import models
from django.contrib import admin


class BatImageInlineAdmin(admin.StackedInline):
    model = models.BatImage


class BatAttributesInlineAdmin(admin.StackedInline):
    model = models.BatAttributes


@admin.register(models.Bat)
class BatAdmin(admin.ModelAdmin):
    list_display = ("name", "is_in_red_book", "genus", "updated_at")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [BatImageInlineAdmin, BatAttributesInlineAdmin]


@admin.register(models.Genus)
class GenusModel(admin.ModelAdmin):
    list_display = ("name", "family", "updated_at")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(models.Family)
class FamilyModel(admin.ModelAdmin):
    list_display = ("name", "updated_at")
    prepopulated_fields = {"slug": ("name",)}
