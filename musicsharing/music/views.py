from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import User, MusicFile, Access

@login_required
def home(request):
    music_files = MusicFile.objects.filter(
        models.Q(privacy='public') |
        models.Q(user=request.user) |
        models.Q(access__user=request.user)
    ).distinct()
    return render(request, 'music/home.html', {'music_files': music_files})

@login_required
def upload(request):
    if request.method == 'POST':
        name = request.POST['name']
        file = request.FILES['file']
        privacy = request.POST['privacy']
        music_file = MusicFile(user=request.user, name=name, file=file, privacy=privacy)
        music_file.save()
        if privacy == 'protected':
            allowed_emails = [email.strip() for email in request.POST['allowed_emails'].split(',')]
            for email in allowed_emails:
                try:
                    user = User.objects.get(email=email)
                    access = Access(music_file=music_file, user=user)
                    access.save()
                except User.DoesNotExist:
                    pass
        messages.success(request, 'Music file uploaded successfully!')
        return redirect('music:home')
    return render(request, 'music')
