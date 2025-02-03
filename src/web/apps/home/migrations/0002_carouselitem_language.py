# Generated by Django 5.1.5 on 2025-02-03 17:18

import apps.shared.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='carouselitem',
            name='language',
            field=apps.shared.models.LanguageField(choices=[('az', 'Azerbaijani'), ('en', 'English')], default='az', max_length=2),
        ),
    ]
