from django.urls import path

from DB_client.views import *

urlpatterns = [
    path("", index, name="home"),
    path("start_page/", StartPage.as_view(), name="start_page"),
    path("register/", RegisterUser.as_view(), name="register"),
    path("login/", LoginUser.as_view(), name="login"),
]