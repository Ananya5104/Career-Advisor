from typing import Dict,List, Set,Union

def normalize_skills(skills: Union[str, List, Set]) -> Set[str]:
    
    if isinstance(skills, str):
        # Handle comma-separated string
        return {skill.strip().lower() for skill in skills.split(',') if skill.strip()}
    elif isinstance(skills, (list, set)):
        # Handle list or set of skills
        return {str(skill).strip().lower() for skill in skills if str(skill).strip()}
    else:
        raise ValueError(f"Invalid skills format: {type(skills)}. Expected string, list, or set.")

def calculate_job_match_score(user_skills: Dict, job: Dict) -> Dict:
   
    try:
        # Normalize and combine user technical and soft skills
        tech_skills = normalize_skills(user_skills.get('technical_skills', []))
        soft_skills = normalize_skills(user_skills.get('soft_skills', []))
        user_all_skills = tech_skills.union(soft_skills)
        
        # Normalize job required skills
        job_skills = normalize_skills(job.get('skills_required', []))
        
        # Calculate matching and missing skills
        matching_skills = job_skills.intersection(user_all_skills)
        missing_skills = job_skills - user_all_skills
        
        # Handle edge case of no required skills
        if len(job_skills) == 0:
            return {
                'score': 0,
                'matching_skills': [],
                'missing_skills': [],
                'error': 'No required skills specified for the job'
            }
        
        # Calculate match score
        match_score = len(matching_skills) / len(job_skills) * 100
        
        return {
            'score': round(match_score, 2),
            'matching_skills': sorted(list(matching_skills)),
            'missing_skills': sorted(list(missing_skills))
        }
        
    except (ValueError, AttributeError) as e:
        return {
            'score': 0,
            'matching_skills': [],
            'missing_skills': [],
            'error': f'Error processing skills: {str(e)}'
        }


def recommend_jobs(user_skills: Dict, jobs: List) -> List:
    """
    Generate job recommendations based on skills match.
    """
    recommendations = []
    
    for job in jobs:
        match_info = calculate_job_match_score(user_skills, job)
        
        if match_info['score'] > 0:  # Only include jobs with some skill match
            recommendations.append({
                'job': job,
                'match_score': match_info['score'],
                'matching_skills': match_info['matching_skills'],
                'missing_skills': match_info['missing_skills']
            })
    
    # Sort by match score in descending order
    recommendations.sort(key=lambda x: x['match_score'], reverse=True)
    
    return recommendations