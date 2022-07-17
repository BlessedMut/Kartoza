from django.urls import path

from . import views

urlpatterns = [
    path('', views.root, name="profiles-root"),
    path('home/', views.home, name="profiles-home"),
]