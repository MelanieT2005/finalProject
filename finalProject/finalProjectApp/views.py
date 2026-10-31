from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Profile


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
