from apps.home import models
from django.contrib import admin


@admin.register(models.StaticText)
class StaticTextAdmin(admin.ModelAdmin):
    list_display = ('key', 'language')


@admin.register(models.CarouselItem)
class CarouselItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)