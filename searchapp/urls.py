from django.urls import path, reverse_lazy
from searchapp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="volt-home"),
    path("register/", views.register, name="volt-register"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="searchapp/login.html", success_url=reverse_lazy("search")
        ),
        name="volt-login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="searchapp/logout.html"),
        name="volt-logout",
    ),
    path("search/", views.search, name="volt-search"),
]
