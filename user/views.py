from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate


def login(request):
    return render(request, 'user/signin.html', {'title': 'Login'})


def register(request):
    if request == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            messages.success(request, f'Account created successfully for {username}!')
            login(request, user)
            return redirect('profiles-home')
    else:
        form = UserCreationForm()
    return render(request, 'user/signup.html', {'form': form, 'title': 'Register'})
