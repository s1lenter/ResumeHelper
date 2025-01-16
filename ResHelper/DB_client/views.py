from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db import IntegrityError
from django.forms import model_to_dict
from django.shortcuts import render, redirect, get_object_or_404
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
    template_name = 'new_templates/resume_info.html'
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        res_id = self.kwargs.get('res_id')
        user_res = Resume.objects.get(id=res_id)
        print(user_res)
        context['user'] = User.objects.get(id=self.request.user.id)
        context['profile'] = Profile.objects.get(user_id=self.request.user.id)
        context['achievements'] = Achievements.objects.filter(resume=user_res)
        context['addInfo'] = AdditionalInfo.objects.get(resume=user_res)
        context['skill'] = Skill.objects.filter(resume=user_res)
        context['education'] = Education.objects.get(resume=user_res)
        context['work_experience'] = WorkExperience.objects.filter(resume=user_res)
        return context

def logout_user(request):
    logout(request)
    return redirect('start_page')

def create_vacancy(request):
    if request.method == 'POST':
        salary_from = request.POST.get('salary_from')
        if salary_from == '':
            salary_from = None
        salary_to = request.POST.get('salary_to')
        if salary_to == '':
            salary_to = None
        Job.objects.create(employer_id=request.user,
                           name=request.POST.get('name'),
                           company_name=request.POST.get('company'),
                           description=request.POST.get('vacancy-description'),
                           requirements=request.POST.get('requirements'),
                           salary_from=salary_from,
                           salary_to=salary_to,
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

        profession = request.POST.get('interes_profession')
        experience_level = request.POST.get('experience_level')
        desired_salary = request.POST.get('desired_salary')
        personal_qualities = request.POST.get('personal_qualities')

        AdditionalInfo.objects.create(resume=request_res,
                                        profession=profession,
                                        experience_level=experience_level,
                                        desired_salary=desired_salary,
                                        personal_qualities=personal_qualities)

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
    if request.method == 'POST':
        search_word = request.POST.get('search').strip()
        filter_format = request.POST.get('filter_format')
        filter_city = request.POST.get('filter_city')
        filter_exp = request.POST.get('filter_exp')
        print(filter_exp, filter_format, filter_city, search_word)
        vacs = []
        if search_word == '':
            vacs = Job.objects.filter(job_type=filter_format, experience_level=filter_exp, location=filter_city)
        elif search_word == '':
            vacs = Job.objects.filter(name=search_word, job_type=filter_format, experience_level=filter_exp, location=filter_city)
        vacs_list = []
        for vac in vacs:
            vacs_list.append(model_to_dict(vac))
        for vac in vacs_list:
            get_salary_info(vac)
        return render(request, 'new_templates/vacancies.html', {'vacs': vacs_list})

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
    resume = Resume.objects.filter(profile_id=request.user.id)[0]
    get_salary_info(vacancy)
    vacancy['requirements'] = vacancy['requirements'].split(', ')
    if request.method == 'POST':
        Application.objects.create(resume_id=resume.id,
                                   job_id_id=vacancy['id'],
                                   user_id=request.user.id)
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
        if profile.role == 'Employer':
            profile.emp_post = change_model(profile.emp_post, 'emp_post', request)
        user.first_name = change_model(user.first_name, 'first_name', request)
        user.last_name = change_model(user.last_name, 'last_name', request)
        profile.gender = change_model(profile.gender, 'gender', request)
        profile.age = change_model(profile.age, 'age', request)
        user.email = change_model(user.email, 'email', request)
        user.username = change_model(user.username, 'email', request)
        profile.phone_number = change_model(profile.phone_number, 'phone', request)
        profile.social_network = change_model(profile.social_network, 'soc_net', request)
        if request.FILES.getlist('avatar'):
            profile.avatar = request.FILES.getlist('avatar')[0]
        else:
            profile.avatar = profile.avatar

        user.save()
        profile.save()
        return redirect('start_page')

    if profile.role == 'Employer':
        return render(request, 'new_templates/personal_cabinet_work.html', {'user': user, 'profile': profile})
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
    if profile.role == 'Employer':
        data["emp_post"] = profile.emp_post
    for key in data:
        if data[key] is None:
            data[key] = 'Не указано'
    return JsonResponse(data)

def send_resume_data(request):
    resumes = Resume.objects.filter(profile_id=request.user.id)
    data = {}
    for resume in resumes:
        res_data = {}
        edu = Education.objects.get(resume_id=resume.id) #здесь вообще не edu
        res_data['edu_place'] = edu.place
        res_data['edu_level'] = edu.level
        res_data['end_edu_date'] = edu.year
        data[resume.id] = res_data
    return JsonResponse(data)

def delete_resume(request, res_id):
    profile = Profile.objects.get(user_id=request.user.id)
    instance = get_object_or_404(Resume, id=res_id)

    if profile.role == 'Job_Seeker':
        instance.delete()
        return redirect('personal_cabinet')
    else:
        return redirect('personal_cabinet')


def send_vacancy_data(request):
    vacs = Job.objects.filter(employer_id=request.user.id)
    data = {}
    for vac in vacs:
        vac_data = {}
        vac = model_to_dict(vac)
        get_salary_info(vac)
        vac_data['name'] = vac['name']
        vac_data['company_name'] = vac['company_name']
        vac_data['salary_info'] = vac['salary_info']
        vac_data['location'] = vac['location']
        data[vac['id']] = vac_data
    return JsonResponse(data)


def delete_vac(request, vac_id):
    profile = Profile.objects.get(user_id=request.user.id)
    instance = get_object_or_404(Job, id=vac_id)

    if profile.role == 'Employer':
        instance.delete()
        return redirect('personal_cabinet')
    else:
        return redirect('personal_cabinet')

def applications(request):
    vacs = Job.objects.filter(employer_id=request.user.id)
    return render(request, 'new_templates/otkliks.html', {'vacs': vacs})

def check_app(request, vac_id):
    vac = Job.objects.get(id=vac_id)
    apps = Application.objects.filter(job_id_id=vac_id)
    job_seekers = []
    for app in apps:
        user_info = {}
        user_info['user'] = User.objects.get(id=app.user_id)
        user_info['profile'] = Profile.objects.get(user_id=app.user_id)
        user_info['resume'] = Resume.objects.filter(profile_id=app.user_id).last()
        job_seekers.append(user_info)
    return render(request, 'new_templates/otkliks-info.html', {'vac': vac, 'js': job_seekers})

def res_info_emp(request, res_id):
    resume = Resume.objects.get(id=res_id)
    user = User.objects.get(id=resume.profile_id)
    profile = Profile.objects.get(user_id=resume.profile_id)
    context = {}
    context['achievements'] = Achievements.objects.filter(resume_id=resume.id)
    context['skill'] = Skill.objects.filter(resume_id=resume.id)
    context['education'] = Education.objects.get(resume_id=resume.id)
    context['work_experience'] = WorkExperience.objects.filter(resume_id=resume.id)
    context['addInfo'] = AdditionalInfo.objects.get(resume_id=resume.id)
    return render(request, 'new_templates/infoRes.html',
                  {'user': user, 'profile': profile, 'resume': resume,'context': context})


def send_app_vacancy_data(request):
    apps = Application.objects.filter(user_id=request.user.id)
    vacs = {}
    for app in apps:
        vacs[str(app.job_id_id)] = Job.objects.get(id=app.job_id_id)
    data = {}
    print(vacs)
    for vac in vacs.items():
        vac_data = {}
        print(vac[1].salary_from)
        vac_sal = {'salary_from':vac[1].salary_from,'salary_to':vac[1].salary_to}
        get_salary_info(vac_sal)
        vac_data['name'] = vac[1].name
        vac_data['company_name'] = vac[1].company_name
        vac_data['salary_info'] = vac_sal['salary_info']
        vac_data['location'] = vac[1].location
        data[vac[1].id] = vac_data
    print(data)
    return JsonResponse(data)

