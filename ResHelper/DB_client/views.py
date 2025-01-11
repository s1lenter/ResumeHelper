from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db import IntegrityError
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import *
import requests
from .api_handler import *

from .forms import *
from .models import *

from django.conf import settings

def main_view(request):
    return redirect(settings.DEFAULT_REDIRECT_URL)

def start_page(request):
    if request.user.id:
        user_profile = Profile.objects.get(user=request.user)
        return redirect('personal_cabinet')
    return render(request, "new_templates/main_page.html")

def prelogin_page(request):
    return render(request, "new_templates/page.html")

def prelogin_page_work(request):
    return render(request, "new_templates/work_page.html")

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'new_templates/registration.html'
    success_url = None

    def get_success_url(self):
        return reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            try:
                user = form.save()
                Profile.objects.create(user=user, role='Job_Seeker')
                return redirect(self.get_success_url())

            except IntegrityError:
                messages.error(request, 'Пользователь с такой почтой уже существует.')
                return render(request, self.template_name, {'form': form})

        return render(request, self.template_name, {'form': form})

class RegisterUserWork(CreateView):
    form_class = RegisterUserForm
    template_name = 'new_templates/registartion_work.html'
    success_url = None

    def get_success_url(self):
        return reverse_lazy('login_work')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            try:
                user = form.save()
                Profile.objects.create(user=user, role='Employer')
                return redirect(self.get_success_url())

            except IntegrityError:
                messages.error(request, 'Пользователь с такой почтой уже существует.')
                return render(request, self.template_name, {'form': form})

        return render(request, self.template_name, {'form': form})

class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'new_templates/enter.html'

    def get_success_url(self):
        return reverse_lazy('personal_cabinet')

class LoginUserWork(LoginView):
    form_class = AuthenticationForm
    template_name = 'new_templates/enter_work.html'

    def get_success_url(self):
        return reverse_lazy('personal_cabinet')

class ResInfo(ListView):
    template_name = 'res_info.html'
    model = User

    def get_context_data(self, **kwargs):
        user_res = Resume.objects.filter(profile=self.request.user).last()  #пока что возвращается последнее созданное резюме
        print(Achievements.objects.filter(resume=user_res))
        context = super().get_context_data(**kwargs)

        context['achievements'] = Achievements.objects.filter(resume=user_res)[0]

        context['skill'] = Skill.objects.filter(resume=user_res)[0]
        context['education'] = Education.objects.filter(resume=user_res)[0]
        context['work_experience'] = WorkExperience.objects.filter(resume=user_res)[0]
        return context

def logout_user(request):
    logout(request)
    return redirect('start_page')

def create_vacancy(request):
    if request.method == 'POST':
        Job.objects.create(employer_id=request.user,
                           name=request.POST.get('name'),
                           company_name=request.POST.get('company'),
                           description=request.POST.get('vacancy-description'),
                           requirements=request.POST.get('requirements'),
                           salary_from=request.POST.get('salary_from'),
                           salary_to=request.POST.get('salary_to'),
                           conditions=request.POST.get('conditions'),
                           location=request.POST.get('area'),
                           job_type=request.POST.get('work_type'),
                           experience_level=request.POST.get('work_experience'),
                           created_at=datetime.datetime.now(),
                           updated_at=datetime.datetime.now())
        return redirect('start_page')
    user_role = Profile.objects.filter(user=request.user)[0].role
    if user_role == 'Job_Seeker':
        return render(request, 'new_templates/403-page.html')
    return render(request, 'new_templates/make_vacancy.html')

def create_resume(request):
    if request.method == 'POST':
        Resume.objects.create(profile=request.user, created_at=datetime.datetime.now())
        request_res = Resume.objects.filter(profile=request.user).last()
        images = request.FILES.getlist('ach_image')
        for image in images:
            Achievements.objects.create(ach_image=image, resume=request_res)
        skills = request.POST.getlist('skill')
        for skill in skills:
            Skill.objects.create(skill_name=skill, resume=request_res)
        edu_level = request.POST.get('level')
        place = request.POST.get('education-place')
        year = request.POST.get('education-date')
        Education.objects.create(resume=request_res,
                                 level=edu_level,
                                 place=place,
                                 year=year)
        prof = request.POST.getlist('profession')
        comp = request.POST.getlist('company')
        start_date = request.POST.getlist('startdate')
        end_date = request.POST.getlist('enddate')

        for i in range(len(prof)):
            WorkExperience.objects.create(resume=request_res,
                                          job_title=prof[i],
                                          company=comp[i],
                                          start_date=start_date[i],
                                          end_date=end_date[i])
        return redirect('start_page')
    user_role = Profile.objects.filter(user=request.user)[0].role
    if user_role == 'Employer':
        return render(request, 'new_templates/403-page.html')
    return render(request, 'make_resume.html')

# def vacs_view(request):
#     vacancies = get_vacancies(5)
#     return render(request, 'vacancies.html', {'vacs': vacancies.items()})

def vacancies(request):
    vacs = Job.objects.all().values()
    for vac in vacs:
        get_salary_info(vac)
    return render(request, 'new_templates/vacancies.html', {'vacs': vacs})

def get_salary_info(vac):
    if vac['salary_from'] is not None and vac['salary_to'] is not None:
        vac['salary_info'] = f'От {vac["salary_from"]} до {vac["salary_to"]} рублей'
    elif vac['salary_from'] is None and vac['salary_to'] is not None:
        vac['salary_info'] = f'До {vac["salary_to"]} рублей'
    elif vac['salary_from'] is not None and vac.salary_to is None:
        vac['salary_info'] = f'От {vac["salary_from"]} рублей'
    else:
        vac['salary_info'] = 'Зарплата не указана'

def vacancy_detail(request, vac_id):
    vacancy = model_to_dict(Job.objects.get(id=vac_id))
    get_salary_info(vacancy)
    vacancy['requirements'] = vacancy['requirements'].split(', ')
    print(vacancy)
    return render(request, 'new_templates/vacancy_info.html', {'vacancy': vacancy})

def about (request):
    return render(request, 'about.html')

def contacts (request):
    return render(request, 'contacts.html')

def change_model(field, field_name, request):
    if request.POST.get(field_name) != '':
        return request.POST.get(field_name)
    else:
        return field

def personal_cabinet (request):
    user = User.objects.get(id=request.user.id)
    profile = Profile.objects.get(user_id=request.user.id)
    if request.method == 'POST':
        user.first_name = change_model(user.first_name, 'first_name', request)
        user.last_name = change_model(user.last_name, 'last_name', request)
        profile.gender = change_model(profile.gender, 'gender', request)
        profile.age = change_model(profile.age, 'age', request)
        profile.email = change_model(profile.email, 'email', request)
        profile.phone_number = change_model(profile.phone, 'phone', request)
        profile.social_network = change_model(profile.soc_net, 'soc_net', request)
        if request.FILES.getlist('avatar'):
            profile.avatar = request.FILES.getlist('avatar')[0]
        else:
            profile.avatar = profile.avatar

        user.save()
        profile.save()

    if profile.role == 'Employer':
        return render(request, 'new_templates/personal_cabinet_work.html', {'user': user})
    else:
        return render(request, 'new_templates/personal_cabinet.html', {'user': user, 'profile': profile})


def send_personal_data(request):
    user = User.objects.get(id=request.user.id)
    profile = Profile.objects.get(user_id=user.id)
    data = {
        "email": user.email,
        "phone": profile.phone_number,
        "socNetwork": profile.social_network,
        "sex": profile.gender,
        "age": profile.age,
    }
    for key in data:
        if data[key] is None:
            data[key] = 'Не указано'
    return JsonResponse(data)