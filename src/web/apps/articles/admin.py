from django.contrib import admin
from apps.articles import models

# Register your models here.
@admin.register(models.Article)
class ArticleModel(admin.ModelAdmin):
    list_display = ('name', 'author', 'url')
    readonly_fields = ('created_at', 'updated_at')