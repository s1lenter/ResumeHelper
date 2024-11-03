from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound
from .models import User

def register(request):
    return render(request, "registration.html")

def start_page(request):
    return render(request, "start_page.html")

# получение данных из бд
def index(request):
    people = User.objects.all()
    return render(request, "index.html", {"people": people})


# сохранение данных в бд
def create(request):
    if request.method == "POST":
        person = User()
        person.First_Name = request.POST.get("First_Name")
        person.Last_Name = request.POST.get("Last_Name")
        person.save()
    return HttpResponseRedirect("/")


#изменение данных в бд
def edit(request, id):
    try:
        person = User.objects.get(id=id)

        if request.method == "POST":
            person.First_Name = request.POST.get("First_Name")
            person.Second_Name = request.POST.get("Second_Name")
            person.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, "edit.html", {"person": person})
    except User.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


# удаление данных из бд
def delete(request, id):
    try:
        person = User.objects.get(id=id)
        person.delete()
        return HttpResponseRedirect("/")
    except User.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")

