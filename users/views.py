from django.shortcuts import render
from .forms import ResumeUploadForm

def upload_resume(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return render(request, 'upload_success.html')
    else:
        form = ResumeUploadForm()
    return render(request, 'upload_resume.html', {'form': form})
