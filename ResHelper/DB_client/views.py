from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from .forms import RegisterUserForm
from .models import *

# def register(request):
#     people = User.objects.all()
#     return render(request, "registration.html", {"people":people})

# получение данных из бд
# def start_page(request):
#     return render(request, "start_page.html")

class StartPage(ListView):
    model = User
    template_name = 'start_page.html'

def index(request):
    people = User.objects.all()
    return render(request, "index.html", {"people": people})


# сохранение данных в бд
def create(request):
    if request.method == "POST":
        person = User()
        person.first_name = request.POST.get("first_name")
        person.last_name = request.POST.get("last_name")
        person.email = request.POST.get("email")
        person.password_hash = request.POST.get("password_hash")
        person.save()
    return redirect("/login/")

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
        return reverse_lazy('start_page')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        is_valid = True
        # for f in form:
        #     if f.errors:
        #         is_valid = False
        #         break
        # if len(form.cleaned_data['password1']) < 8:
        #     form.add_error('password1', 'Пароль должен содержать не менее 8 символов.')
        if User.objects.filter(email=request.POST.get('email')).exists() or not form.is_valid():
            messages.error(request, 'Пользователь с такой почтой уже существует.')
            return render(request, self.template_name, {'form': form})
        form.save()
        return redirect(self.get_success_url())

class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'login1.html'

    def get_success_url(self):
        return reverse_lazy('start_page')
