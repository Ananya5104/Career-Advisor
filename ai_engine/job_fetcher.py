import re
from typing import List,Dict
import requests
import spacy
from django.core.cache import cache

ADZUNA_API_URL = "https://api.adzuna.com/v1/api/jobs"
APP_ID = "278c3aed"
APP_KEY = "a50e47724dc2b09f2ee6bc1ecc8df101"


def extract_skills_from_job(job_description: str) -> List[str]:
    """
    Extract skills from job description using NLP.
    """
    nlp = spacy.load("en_core_web_sm")
    
    # Define common skills
    common_skills = [
        'python', 'java', 'javascript', 'html', 'css', 'sql', 'aws', 
        'docker', 'kubernetes', 'react', 'angular', 'node.js', 'mongodb',
        'machine learning', 'data analysis', 'ai', 'git', 'devops',
        'c++', 'ruby', 'php', 'scala', 'swift', 'typescript'
    ]
    
    # Create patterns for skill matching
    skill_patterns = [
        re.compile(r'\b' + re.escape(skill) + r'\b', re.IGNORECASE)
        for skill in common_skills
    ]
    
    # Extract skills from text
    found_skills = set()
    for pattern in skill_patterns:
        matches = pattern.finditer(job_description.lower())
        for match in matches:
            found_skills.add(match.group())
            
    return list(found_skills)

def extract_skills_from_text(text: str) -> List[str]:
    """
    Extract skills from job description text using NLP.
    """
    nlp = spacy.load("en_core_web_sm")
    
    # Define common skills (you can expand this list)
    common_skills = [
        'python', 'java', 'javascript', 'html', 'css', 'sql', 'aws', 
        'docker', 'kubernetes', 'react', 'angular', 'node.js', 'mongodb',
        'machine learning', 'data analysis', 'ai', 'git', 'devops'
    ]
    
    # Create patterns for skill matching
    skill_patterns = [
        re.compile(r'\b' + re.escape(skill) + r'\b', re.IGNORECASE)
        for skill in common_skills
    ]
    
    # Extract skills from text
    found_skills = set()
    for pattern in skill_patterns:
        matches = pattern.finditer(text.lower())
        for match in matches:
            found_skills.add(match.group())
            
    return list(found_skills)
    

def fetch_all_jobs(query='software engineer', location='remote'):
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": 100,
        "what": query,
        "where": location,
    }
    url = f"{ADZUNA_API_URL}/us/search/1"  
    print(url)
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return [
            {
                "title": job["title"],
                "company": job["company"]["display_name"],
                "location": job["location"]["display_name"],
                "description": job["description"],
                "skills_required": job["category"]["label"],
            }
            for job in data.get("results", [])
        ]
    else:
        print(f"Error fetching jobs: {response.status_code} - {response.text}")
        return []

from django.core.cache import cache

def fetch_all_jobs_cached(query='', location=''):
    cache_key = f"jobs_{query}_{location}"
    jobs = cache.get(cache_key)
    if jobs is None:
        jobs = fetch_all_jobs(query, location)
        cache.set(cache_key, jobs, timeout=3600)  # Cache for 1 hour
    return jobs
