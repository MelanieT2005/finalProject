from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import Profile


def home(request):
    return render(request, 'finalProjectApp/home.html')


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user)

    return render(request, 'finalProjectApp/profile.html', {'profile': profile})


@login_required
def edit_profile(request, username):
    user = get_object_or_404(User, username=username)

    if request.user != user:
        raise PermissionDenied

    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        profile.bio = request.POST.get('bio', '')

        if request.POST.get('remove_picture') == 'on':
            profile.profile_picture.delete(save=False)
            profile.profile_picture = None

        elif 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']

        profile.save()

        return redirect('profile', username=username)

    return render(request, 'finalProjectApp/edit_profile.html', {'profile': profile})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')

    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)

    return redirect('login')
