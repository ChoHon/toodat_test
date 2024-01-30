from django.urls import path
from .views import *

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),

    path("login-page/", LoginPage, name="login-page"),
    path("signup-page/", SignupPage, name="signup-page"),
]