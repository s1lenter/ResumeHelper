import datetime

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse
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
    return render(request, "new_templates/main_page.html")

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'registration.html'
    success_url = None

    def get_success_url(self):
        return reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            try:
                form.save()
                return redirect(self.get_success_url())

            except IntegrityError:
                messages.error(request, 'Пользователь с такой почтой уже существует.')
                return render(request, self.template_name, {'form': form})

        return render(request, self.template_name, {'form': form})

class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'login1.html'

    def get_success_url(self):
        return reverse_lazy('start_page')

# class CreateVacancy(ListView):
#     template_name = 'make_vacancy.html'
#     model = User

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
                           conditions=request.POST.get('conditions'),
                           location=request.POST.get('area'),
                           job_type=request.POST.get('work_type'),
                           experience_level=request.POST.get('work_experience'),
                           created_at=datetime.datetime.now(),
                           updated_at=datetime.datetime.now())
        return redirect('start_page')
    return render(request, 'make_vacancy.html')

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
    else:
        form = ResumeForm()
    return render(request, 'make_resume.html', {'from': form})

def vacs_view(request):
    vacancies = get_vacancies(5)
    return render(request, 'vacancies.html', {'vacs': vacancies.items()})

def about (request):
    return render(request, 'about.html')

def contacts (request):
    return render(request, 'contacts.html')

def personal_cabinet (request):
    return render(request, 'personal_cabinet.html')

