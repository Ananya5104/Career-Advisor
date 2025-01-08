from django.urls import path
from .views import job_list,job_recommendations

urlpatterns = [
    path('', job_list, name='job_list'),
    path('recommendations/', job_recommendations, name='job_recommendations'),
]
