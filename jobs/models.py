from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    skills_required = models.TextField()  # Comma-separated skills
    posted_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
