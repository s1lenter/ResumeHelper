import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.template.defaultfilters import default

class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    age = models.IntegerField(null=True)
    role = models.CharField(max_length=20)
    email = models.EmailField(null=True)
    password_hash = models.CharField(max_length=255, default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default = datetime.date.today())
    updated_at = models.DateTimeField(auto_now=True)


class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.JSONField()
    conditions = models.TextField()
    location = models.CharField(max_length=100)
    job_type = models.CharField(
        max_length=10,
        choices=[
            ('Full_Time', 'Full Time'),
            ('Part_Time', 'Part Time'),
            ('Remote', 'Remote')
        ]
    )
    experience_level = models.CharField(
        max_length=10,
        choices=[
            ('Junior', 'Junior'),
            ('Mid', 'Mid'),
            ('Senior', 'Senior')
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    contact_info = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Settings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    preferences = models.JSONField()


class Application(models.Model):
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=[
            ('Pending', 'Pending'),
            ('Rejected', 'Rejected'),
            ('Accepted', 'Accepted')
        ],
        default='Pending'
    )


class Achievements(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    description = models.TextField()


class Skill(models.Model):
    skill_name = models.CharField(max_length=100)


class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    year = models.IntegerField(
        verbose_name='Год',
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(datetime.date.today().year)
        ]
    )

class WorkExperience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()