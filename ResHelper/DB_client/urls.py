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
    path("res_info/<int:res_id>/", ResInfo.as_view(), name="res_info"),
    path("vacancies/", vacancies, name="vacancies"),
    path("about/", about, name="about"),
    path("contacts/", contacts, name="contacts"),
    path("personal_cabinet/", personal_cabinet, name="personal_cabinet"),
    path("api/personal_data/", send_personal_data, name="personal_data"),
    path("api/resume_data/", send_resume_data, name="resume_data"),
    path("api/vacancy_data/", send_vacancy_data, name="vacancy_data"),
    path("api/app_vacancy_data/", send_app_vacancy_data, name="app_vacancy_data"),
    path("vacancy_detail/<int:vac_id>/", vacancy_detail, name="vacancy_detail"),
    path("delete_resume/<int:res_id>/", delete_resume, name="delete_resume"),
    path("delete_vac/<int:vac_id>/", delete_vac, name="delete_vac"),
    path("applications/", applications, name="applications"),
    path("check_app/<int:vac_id>/", check_app, name="check_app"),
    path("res_info_emp/<int:res_id>/", res_info_emp, name="res_info_emp"),
    path("work_vacs_detail/<int:vac_id>/", js_vacancy_detail,name="work_vacs_detail")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
