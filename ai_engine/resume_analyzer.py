import spacy
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import re
from typing import List, Dict
import PyPDF2
import os

def analyze_resume(pdf_path: str) -> Dict:
    """
    Extract skills from a PDF resume using NLP.
    """
    # Validate file
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"File not found: {pdf_path}")
    if not pdf_path.lower().endswith('.pdf'):
        raise ValueError("File must be a PDF")

    # Load spaCy model
    nlp = spacy.load("en_core_web_sm")
    
    # Read PDF file
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            resume_text = ''
            for page in pdf_reader.pages:
                resume_text += page.extract_text()
    except Exception as e:
        raise Exception(f"Error reading PDF file: {str(e)}")
    
    # Clean the resume text
    def clean_text(text):
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.lower().strip()
    
    cleaned_text = clean_text(resume_text)
    
    # Define skills to look for
    default_tech_skills = [
        'python', 'java', 'javascript', 'html', 'css', 'sql', 'aws', 
        'docker', 'kubernetes', 'react', 'angular', 'node.js', 'mongodb',
        'machine learning', 'data analysis', 'ai', 'git', 'devops',
        'c++', 'ruby', 'php', 'scala', 'swift', 'typescript'
    ]
    
    default_soft_skills = [
        'leadership', 'communication', 'teamwork', 'problem solving',
        'project management', 'time management', 'analytical', 'creativity',
        'collaboration', 'adaptability', 'organization', 'critical thinking'
    ]
    
    all_skills = set(default_tech_skills + default_soft_skills)
    
    # Create skill patterns
    skill_patterns = [
        re.compile(r'\b' + re.escape(skill) + r'\b', re.IGNORECASE)
        for skill in all_skills
    ]
    
    # Find skills
    found_skills = {
        'technical_skills': [],
        'soft_skills': [],
        'skill_frequency': {}
    }
    
    for pattern in skill_patterns:
        matches = pattern.finditer(cleaned_text)
        for match in matches:
            skill = match.group().lower()
            if skill in default_tech_skills:
                found_skills['technical_skills'].append(skill)
            elif skill in default_soft_skills:
                found_skills['soft_skills'].append(skill)
                
    # Count frequencies and remove duplicates
    found_skills['technical_skills'] = sorted(list(set(found_skills['technical_skills'])))
    found_skills['soft_skills'] = sorted(list(set(found_skills['soft_skills'])))
    
    return found_skills
