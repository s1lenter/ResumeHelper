import datetime

from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from django.template.defaultfilters import default
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(
        max_length=10,
        choices=[
            ('Male', 'Мужской'),
            ('Female', 'Женский'),
            ('Other', 'Другое')
        ],
        null=True
    )
    age = models.IntegerField(null=True)
    role = models.CharField(
        max_length=20,
        choices=[
            ('Job_Seeker', 'Соискатель'),
            ('Employer', 'Работодатель')
        ],
        default='Job_Seeker')
    social_network = models.TextField(null=True)
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                   message="Введите правильный номер телефона в формате: '+999999999'. До 15 цифр.")],
        null=True
    )
    avatar = models.ImageField(upload_to='avatars/', null=True)



class Job(models.Model):
    employer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.JSONField()
    conditions = models.TextField()
    salary_from = models.DecimalField(max_digits=8, decimal_places=0, null=True)
    salary_to = models.DecimalField(max_digits=8, decimal_places=0, null=True)
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
        max_length=20,
        choices=[
            ('no_expirience', 'Без опыта'),
            ('1_between_3', 'От 1 года до 3 лет'),
            ('3_between_6', 'От 3 до 6 лет'),
            ('more_than_6', 'От 3 до 6 лет'),
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Resume(models.Model):
    profile = models.ForeignKey(User, on_delete=models.CASCADE)
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
    ach_image = models.ImageField(upload_to='photos/', default=None)


class Skill(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=100)


class Education(models.Model):
    level = models.CharField(
        max_length=25,
        choices=[
            ('secondary', 'Среднее'),
            ('secondary-specialised', 'Среднее специальное'),
            ('uncompleted-higher', 'Неоконченное высшее'),
            ('higher', 'Высшее'),
            ('bachelor', 'Бакалвар'),
            ('master', 'Магистр'),
            ('Ph', 'Кандидат наук'),
            ('PhD', 'Доктор наук'),
        ],
        default='Среднее'
    )
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    place = models.CharField(max_length=100)
    year = models.CharField(max_length=10,
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
    start_date = models.CharField(max_length=10)
    end_date = models.CharField(max_length=10)

class AdditionalInfo(models.Model):
    desired_salary = models.DecimalField(max_digits=8, decimal_places=0, null=True)
    personal_qualities = models.TextField()
    experience_level = models.CharField(
        max_length=20,
        choices=[
            ('no_expirience', 'Без опыта'),
            ('1_between_3', 'От 1 года до 3 лет'),
            ('3_between_6', 'От 3 до 6 лет'),
            ('more_than_6', 'От 3 до 6 лет'),
        ]
    )