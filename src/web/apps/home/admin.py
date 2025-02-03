from apps.home.models import CarouselItem, StaticText
from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _
from tinymce.widgets import TinyMCE


@admin.register(StaticText)
class StaticTextAdmin(admin.ModelAdmin):
    list_display = ("key", "language")
    formfield_overrides = {models.TextField: {"widget": TinyMCE()}}


@admin.register(CarouselItem)
class CarouselItemAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "image_extension")
    list_editable = ("order",)


admin.site.site_header = _("Administration")
admin.site.site_title = _("Administration")
admin.site.index_title = _("Welcome to the Administration")
