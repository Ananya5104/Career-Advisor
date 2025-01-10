from django.shortcuts import render, redirect
from .forms import ResumeUploadForm, CustomUserCreationForm
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()

def upload_resume(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            # Prevent saving a duplicate email
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exclude(pk=request.user.pk).exists():
                form.add_error('email', 'A user with this email already exists.')
            else:
                form.save()
                return redirect('job_recommendations')
    else:
        form = ResumeUploadForm(instance=request.user)
    return render(request, 'upload_resume.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('landing')


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created! You can now log in.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})