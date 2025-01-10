import hashlib
from django.shortcuts import render
from .models import Job
from ai_engine.recommendation_engine import  calculate_job_match_score,recommend_jobs
from users.models import CustomUser
from ai_engine.job_fetcher import  extract_skills_from_job,fetch_all_jobs
from ai_engine.resume_analyzer import analyze_resume
from django.core.cache import cache


def job_list(request):
    jobs = fetch_all_jobs(query='', location='')
    return render(request, 'job_list.html', {'jobs': jobs})



def job_recommendations(request):
    """
    View function to handle job recommendations based on user's resume.
    """
    user = request.user
    page = request.GET.get('page', 1)
    
    if not user.resume:
        return render(request, 'no_resume.html')
    
    try:
        # Extract skills from resume
        resume_path = user.resume.path
        user_skills =  analyze_resume(resume_path)
        
        # Fetch jobs from API
        jobs = fetch_all_jobs(query='software engineer', location='remote')
        print(len(jobs))
        
        # Generate recommendations
        recommendations = []
        for job in jobs:
            match_info = calculate_job_match_score(user_skills, job)
            if match_info['score'] >= 0.0:  
                recommendations.append({
                    'job': job,
                    'match_score': match_info['score'],
                    'matching_skills': match_info['matching_skills'],
                    'missing_skills': match_info['missing_skills']
                })
        
        # Sort by match score
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        # print(recommendations)
        
        context = {
            'recommendations': recommendations,
            'user_skills': user_skills,
            'total_jobs_matched': len(recommendations),
            'current_page': page,
            'has_next': len(jobs) == 20  # Assuming 20 results per page
        }
        # print(context)
        return render(request, 'job_recommendations.html', context)
    
    except Exception as e:
        error_message = f"Error processing request: {str(e)}"
        print(error_message)  # For logging
        return render(request, 'error.html', {'message': error_message})
