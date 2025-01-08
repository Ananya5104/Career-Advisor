from django.shortcuts import render, redirect
from .forms import ResumeUploadForm

def upload_resume(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('job_recommendations')
    else:
        form = ResumeUploadForm(instance=request.user)
    return render(request, 'upload_resume.html', {'form': form})
