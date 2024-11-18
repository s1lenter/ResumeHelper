from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist

from .models import *


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        send = super(RegisterUserForm, self).save(commit=False)
        send.username = send.email
        if commit:
            send.save()
        return send

class AddPersonalInfoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['gender', 'age', 'phone_number']

class ChangeUserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class UserInfoForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    age = forms.IntegerField(required=False)
    gender = forms.ChoiceField(choices=[('Male', 'Мужской'), ('Female', 'Женский')], required=False)
    phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$', required=False)

    def clean(self):
        cleaned_data = super().clean()

        # Получаем ID пользователя из запроса (предполагается, что оно передается в view)
        user_id = self.initial.get('user_id')

        try:
            # Получаем существующего пользователя
            user = User.objects.get(id=user_id)

            # Обновляем поля пользователя
            if cleaned_data.get('first_name'):
                user.first_name = cleaned_data['first_name']
            if cleaned_data.get('last_name'):
                user.last_name = cleaned_data['last_name']
            if cleaned_data.get('email'):
                user.email = cleaned_data['email']

            user.save()

            # Обновляем профиль
            profile, created = Profile.objects.update_or_create(
                user=user,
                defaults={
                    'age': cleaned_data.get('age'),
                    'gender': cleaned_data['gender'],
                    'phone_number': cleaned_data.get('phone_number')
                }
            )

            # Сохраняем обновленные данные профиля
            if created or (profile.age != cleaned_data.get('age') or
                           profile.gender != cleaned_data['gender'] or
                           profile.phone_number != cleaned_data.get('phone_number')):
                profile.save()

        except ObjectDoesNotExist:
            raise forms.ValidationError("Пользователь с указанным ID не найден." + str(user_id))

        return cleaned_data