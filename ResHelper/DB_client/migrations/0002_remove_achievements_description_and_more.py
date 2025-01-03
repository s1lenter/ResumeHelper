# Generated by Django 5.1.2 on 2025-01-03 07:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DB_client', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='achievements',
            name='description',
        ),
        migrations.AddField(
            model_name='achievements',
            name='ach_image',
            field=models.ImageField(default=None, upload_to=''),
        ),
        migrations.AlterField(
            model_name='education',
            name='year',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1940), django.core.validators.MaxValueValidator(2025)], verbose_name='Год'),
        ),
    ]