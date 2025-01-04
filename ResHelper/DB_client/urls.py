from django.urls import path
from django.conf.urls.static import static
from DB_client.views import *

urlpatterns = [
    path("", main_view, name="home"), #перенаправление через settings
    path("start_page/", StartPage.as_view(), name="start_page"),
    path("register/", RegisterUser.as_view(), name="register"),
    path("login/", LoginUser.as_view(), name="login"),
    path("logout/", logout_user, name="logout"),
    path("create_resume/", create_resume, name="create_resume"),
    path("create_vacancy/", create_vacancy, name="create_vacancy"),
    path("res_info/", ResInfo.as_view(), name="res_info"),
    path("vac_test/", vacs_view, name="vacs_view"),
    path("about/", about, name="about"),
    path("contacts/", contacts, name="contacts"),
    path("personal_cabinet/", personal_cabinet, name="personal_cabinet")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
