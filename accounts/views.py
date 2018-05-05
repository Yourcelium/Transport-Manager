from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('schedule: index')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def index(request):
    return render(request, 'index.html')