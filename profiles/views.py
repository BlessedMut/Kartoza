from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def root(request):
    return render(request, 'profiles/index.html', {})


def home(request):
    return render(request, 'profiles/home/home.html', {'title': 'Home'})


@login_required
def profile(request):
    return render(request, 'profiles/home/profile.html', {'title': 'Profile'})
