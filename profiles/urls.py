from django.urls import path

from . import views as profile_views

urlpatterns = [
    path('', profile_views.root, name="profiles-root"),
    path('user/home/', profile_views.home, name="profiles-home"),
    path('user/profile/', profile_views.profile, name="profiles-settings"),
    path('user/profiles/', profile_views.all_profiles, name="profiles-all"),
]