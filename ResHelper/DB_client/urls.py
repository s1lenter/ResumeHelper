from django.urls import path

from DB_client.views import *

urlpatterns = [
    path("", main_view, name="home"), #перенаправление через settings
    path("start_page/", StartPage.as_view(), name="start_page"),
    path("register/", RegisterUser.as_view(), name="register"),
    path("login/", LoginUser.as_view(), name="login"),
    path("logout/", logout_user, name="logout"),
    path("create_resume/", create_resume, name="create_resume"),
    path("create_vacancy/", CreateVacancy.as_view(), name="create_vacancy"),
    path("res_info/", ResInfo.as_view(), name="res_info")
]