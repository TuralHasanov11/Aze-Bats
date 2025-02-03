from apps.home import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


@admin.register(models.StaticText)
class StaticTextAdmin(admin.ModelAdmin):
    list_display = ('key', 'language')


@admin.register(models.CarouselItem)
class CarouselItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'image_extension')
    list_editable = ('order',)
    
    
admin.site.site_header = _("Administration")
admin.site.site_title = _("Administration")
admin.site.index_title = _("Welcome to the Administration")