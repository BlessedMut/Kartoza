from django.urls import path

from . import views as auth_views

urlpatterns = [
    path('login/', auth_views.login_user, name="login"),
    path('logout/', auth_views.logout, name="logout"),
    path('register/', auth_views.register, name="register"),
]