from django.urls import path
from DB_client import views

urlpatterns = [
    path("", views.index),
    path("start_page/", views.start_page),
    path("register/", views.register),
    path("create/", views.create),
    path("login/", views.login),
    path("login/check/", views.check),
    # path("edit/<int:id>/", views.edit),
    # path("delete/<int:id>/", views.delete),
]