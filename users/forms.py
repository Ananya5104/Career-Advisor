from django import forms
from .models import CustomUser

class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['resume']
