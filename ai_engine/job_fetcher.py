import requests

ADZUNA_API_URL = "https://api.adzuna.com/v1/api/jobs"
APP_ID = "278c3aed"
APP_KEY = "a50e47724dc2b09f2ee6bc1ecc8df101"

def fetch_jobs(query="software engineer", location="remote"):
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": 10,
        "what": query,
        "where": location,
    }
    response = requests.get(f"{ADZUNA_API_URL}/us/search/1", params=params)
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
        return []
