import datetime

from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from django.template.defaultfilters import default

class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    gender = models.CharField(
        max_length=10,
        choices=[
            ('Male', 'Мужской'),
            ('Female', 'Женский'),
            ('Other', 'Другое')
        ],
        default='Male'
    )
    age = models.IntegerField(null=True)
    role = models.CharField(
        max_length=20,
        choices=[
            ('Job_Seeker', 'Соискатель'),
            ('Employer', 'Работодатель')
        ],
        default='Job_Seeker')
    password_hash = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                   message="Введите правильный номер телефона в формате: '+999999999'. До 15 цифр.")]
    )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default = datetime.date.today())
    updated_at = models.DateTimeField(auto_now=True)


class Job(models.Model):
    employer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.JSONField()
    conditions = models.TextField()
    location = models.CharField(max_length=100)
    job_type = models.CharField(
        max_length=10,
        choices=[
            ('Full_Time', 'Полная занятость'),
            ('Part_Time', 'Частичная занятость'),
            ('Remote', 'Удалённая работа')
        ]
    )
    experience_level = models.CharField(
        max_length=10,
        choices=[
            ('No_expirience', 'Без опыта'),
            ('1_between_3', 'От 1 года до 3 лет'),
            ('3_between_6', 'От 3 до 6 лет')
            ('more_than_6', 'От 3 до 6 лет')
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Resume(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_info = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Settings(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    preferences = models.JSONField()


class Application(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=[
            ('Pending', 'В ожидании'),
            ('Rejected', 'Отклонено'),
            ('Accepted', 'Принято')
        ],
        default='Pending'
    )


class Achievements(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    description = models.TextField()


class Skill(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=100)


class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    year = models.IntegerField(
        verbose_name='Год',
        validators=[
            MinValueValidator(1940),
            MaxValueValidator(datetime.date.today().year)
        ]
    )

class WorkExperience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()