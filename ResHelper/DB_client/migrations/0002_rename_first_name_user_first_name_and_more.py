# Generated by Django 5.1.2 on 2024-11-02 07:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DB_client', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='First_Name',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='Last_Name',
            new_name='last_name',
        ),
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(default=datetime.date(2024, 11, 2)),
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default=18, max_length=10),
        ),
        migrations.AddField(
            model_name='user',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='password_hash',
            field=models.CharField(default=False, max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('Job_Seeker', 'Job Seeker'), ('Employer', 'Employer')], default='Job_Seeker', max_length=20),
        ),
        migrations.AddField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]