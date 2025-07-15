from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "users"
urlpatterns = [
    path("profile",views.ViewProfileView.as_view(),name="user-profile"),
    path("password_change/", auth_views.PasswordChangeView.as_view(template_name="users/password_change.html"), name="password_change"),
    path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(template_name="users/password_change_done.html"), name="password_change_done"),
]
