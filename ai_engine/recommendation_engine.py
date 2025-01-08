from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend_jobs(user_skills, jobs):
    job_descs = [job.skills_required for job in jobs]
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(job_descs + [user_skills])
    scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    recommendations = sorted(zip(jobs, scores[0]), key=lambda x: x[1], reverse=True)
    return recommendations
