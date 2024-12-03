from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import *

from .forms import *
from .models import *

from django.conf import settings

def main_view(request):
    return redirect(settings.DEFAULT_REDIRECT_URL)

# def register(request):
#     people = User.objects.all()
#     return render(request, "registration.html", {"people":people})

# получение данных из бд
# def start_page(request):
#     return render(request, "start_page.html")

class StartPage(ListView):
    model = User
    template_name = 'start_page.html'

# def index(request):
#     people = User.objects.all()
#     return render(request, "index.html", {"people": people})
#
#
# # сохранение данных в бд
# def create(request):
#     if request.method == "POST":
#         person = User()
#         person.first_name = request.POST.get("first_name")
#         person.last_name = request.POST.get("last_name")
#         person.email = request.POST.get("email")
#         person.password_hash = request.POST.get("password_hash")
#         person.save()
#     return redirect("/login/")

# def login(request):
#     people = User.objects.all()
#     return render(request, "login1.html", {"people": people})

# def check(request):
#     email = request.POST.get('email')
#     password = request.POST.get('password_hash')
#     page = '/'
#     if User.objects.filter(email=email).exists() and User.objects.filter(password_hash=password).exists():
#         page = "/start_page/"
#     return HttpResponseRedirect(page)


# #изменение данных в бд
# def edit(request, id):
#     try:
#         person = User.objects.get(id=id)
#
#         if request.method == "POST":
#             person.First_Name = request.POST.get("First_Name")
#             person.Second_Name = request.POST.get("Second_Name")
#             person.save()
#             return HttpResponseRedirect("/")
#         else:
#             return render(request, "edit.html", {"person": person})
#     except User.DoesNotExist:
#         return HttpResponseNotFound("<h2>Person not found</h2>")
#
#
# # удаление данных из бд
# def delete(request, id):
#     try:
#         person = User.objects.get(id=id)
#         person.delete()
#         return HttpResponseRedirect("/")
#     except User.DoesNotExist:
#         return HttpResponseNotFound("<h2>Person not found</h2>")

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

# class CreateResume(CreateView):
#     model = Profile
#     form_class =
#     template_name = 'login.html'
#
#     def form_valid(self, form):
#         instance = form.save(commit=False)
#         instance.user = self.request.user
#         instance.save()
#
#         return redirect(self.get_success_url())
#
#     def get_success_url(self):
#         return reverse_lazy('start_page')

class CreateVacancy(ListView):
    template_name = 'make_vacancy.html'
    model = User

# class ResInfo(ListView):
#     template_name = 'res_info.html'
#     model = User
#     context_object_name = 'profile'
#     user_id = 0
#
#     def get(self, request, *args, **kwargs):
#         current_user = self.request.user
#         self.user_id = current_user.id
#
#     def get_context_data(self, **kwargs):
#         context = super(ListView, self).get_context_data(**kwargs)
#         context['all_data'] = Profile.objects.get(id=self.user_id)
#         return context

class ResInfo(ListView):
    template_name = 'res_info.html'
    model = User

    # def get(self, request, *args, **kwargs):
    #     response = super().get(request, *args, **kwargs)
    #     current_user = self.request.user
    #     self.user_id = current_user.id
    #     return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user_id=self.request.user.id)
        context['user'] = User.objects.get(id=self.request.user.id)
        return context

def logout_user(request):
    logout(request)
    return redirect('start_page')

def create_resume(request):
    if request.method == 'POST':
        form = UserInfoForm(request.POST, initial={'user_id': request.user.id})
        if form.is_valid():
            return redirect('start_page')
    else:
        form = UserInfoForm(initial={'user': 7})

    return render(request, 'login.html', {'form': form})