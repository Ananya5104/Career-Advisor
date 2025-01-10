from django.urls import path
from .views import upload_resume, login_view, logout_view, signup_view
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('upload-resume/', upload_resume, name='upload_resume'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),
] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
