# Generated by Django 5.1.5 on 2025-02-03 17:01

import apps.activities.models
import apps.shared.models
import django.db.models.manager
import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', apps.shared.models.NameField(max_length=255)),
                ('slug', apps.shared.models.SlugField(blank=True, max_length=255, null=True, unique=True)),
                ('cover_image', models.ImageField(upload_to=apps.activities.models.upload_project_cover_image_to_func, verbose_name='Cover Image')),
                ('description', tinymce.models.HTMLField(verbose_name='Description')),
                ('language', apps.shared.models.LanguageField(choices=[('az', 'Azerbaijani'), ('en', 'English')], default='az', max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update Date')),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
                'ordering': ['-created_at'],
            },
            managers=[
                ('entries', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='SiteVisit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', apps.shared.models.NameField(max_length=255)),
                ('slug', apps.shared.models.SlugField(blank=True, max_length=255, null=True, unique=True)),
                ('cover_image', models.ImageField(upload_to=apps.activities.models.upload_site_visit_cover_image_to_func, verbose_name='Cover Image')),
                ('description', tinymce.models.HTMLField(verbose_name='Description')),
                ('language', apps.shared.models.LanguageField(choices=[('az', 'Azerbaijani'), ('en', 'English')], default='az', max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update Date')),
            ],
            options={
                'verbose_name': 'Site Visit',
                'verbose_name_plural': 'Site Visits',
                'ordering': ['-created_at'],
            },
            managers=[
                ('entries', django.db.models.manager.Manager()),
            ],
        ),
    ]
