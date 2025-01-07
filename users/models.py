from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    linkedin_profile = models.URLField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
