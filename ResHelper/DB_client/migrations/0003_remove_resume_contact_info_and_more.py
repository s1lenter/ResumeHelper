# Generated by Django 5.1.2 on 2025-01-03 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DB_client', '0002_remove_achievements_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resume',
            name='contact_info',
        ),
        migrations.AlterField(
            model_name='achievements',
            name='ach_image',
            field=models.ImageField(default=None, upload_to='photos/'),
        ),
    ]