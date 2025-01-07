from django.urls import path
from django.conf.urls.static import static
from DB_client.views import *

urlpatterns = [
    path("", main_view, name="home"), #перенаправление через settings
    path("start_page/", start_page, name="start_page"),
    path("prelogin_page/", prelogin_page, name="prelogin_page"),
    path("prelogin_page_work/", prelogin_page_work, name="prelogin_page_work"),
    path("register/", RegisterUser.as_view(), name="register"),
    path("register_work/", RegisterUserWork.as_view(), name="register_work"),
    path("login/", LoginUser.as_view(), name="login"),
    path("login_work/", LoginUserWork.as_view(), name="login_work"),
    path("logout/", logout_user, name="logout"),
    path("create_resume/", create_resume, name="create_resume"),
    path("create_vacancy/", create_vacancy, name="create_vacancy"),
    path("res_info/", ResInfo.as_view(), name="res_info"),
    path("vacancies/", vacancies, name="vacancies"),
    path("about/", about, name="about"),
    path("contacts/", contacts, name="contacts"),
    path("personal_cabinet/", personal_cabinet, name="personal_cabinet"),
    path("api/personal_data/", personal_data, name="personal_data"),
    path("vacancy_detail/<int:vac_id>/", vacancy_detail, name="vacancy_detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
