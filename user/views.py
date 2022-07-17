from django.shortcuts import render


def login(request):
    return render(request, 'user/signin.html', {})


def register(request):
    return render(request, 'user/signup.html', {})
