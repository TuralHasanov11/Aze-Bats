# Generated by Django 5.1.5 on 2025-02-03 17:01

import apps.shared.models
import django.db.models.manager
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', apps.shared.models.NameField(max_length=255)),
                ('url', models.URLField(verbose_name='Link')),
                ('author', models.CharField(max_length=255, verbose_name='Author')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update Date')),
            ],
            options={
                'verbose_name': 'Article',
                'verbose_name_plural': 'Articles',
                'ordering': ('-created_at',),
            },
            managers=[
                ('entries', django.db.models.manager.Manager()),
            ],
        ),
    ]
