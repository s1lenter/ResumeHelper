# Generated by Django 5.1.2 on 2025-01-15 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DB_client', '0011_profile_avatar_profile_social_network_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='additionalinfo',
            name='profession',
            field=models.CharField(default='Не указано', max_length=50),
        ),
        migrations.AddField(
            model_name='profile',
            name='emp_post',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='avatars/info_image.png', null=True, upload_to='avatars/'),
        ),
    ]
