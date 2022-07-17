from django.shortcuts import render


def root(request):
    return render(request, 'profiles/index.html', {})


def home(request):
    return render(request, 'profiles/home/home.html', {'title': 'Home'})
