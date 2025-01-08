from django.shortcuts import render
from .models import Job
from ai_engine.recommendation_engine import recommend_jobs
from users.models import CustomUser
from ai_engine.job_fetcher import fetch_jobs
from ai_engine.resume_analyzer import analyze_resume


def job_list(request):
    query = request.GET.get('query', 'software engineer')
    location = request.GET.get('location', 'remote')
    jobs = fetch_jobs(query=query, location=location)
    return render(request, 'job_list.html', {'jobs': jobs})


def job_recommendations(request):
    user = request.user
    if not user.resume:
        return render(request, 'no_resume.html')

    resume_path = user.resume.path  
    user_skills = analyze_resume(resume_path)  
    jobs = Job.objects.all()
    recommendations = recommend_jobs(user_skills, jobs)
    return render(request, 'job_recommendations.html', {
        'recommendations': recommendations,
    })
