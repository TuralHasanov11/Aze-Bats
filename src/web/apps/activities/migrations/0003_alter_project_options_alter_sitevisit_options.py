# Generated by Django 5.1.5 on 2025-02-01 22:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0002_alter_project_cover_image_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-created_at'], 'verbose_name': 'Project', 'verbose_name_plural': 'Projects'},
        ),
        migrations.AlterModelOptions(
            name='sitevisit',
            options={'ordering': ['-created_at'], 'verbose_name': 'Site Visit', 'verbose_name_plural': 'Site Visits'},
        ),
    ]
