from django.urls import path
from .views import generate_leads

urlpatterns = [
    path('generate-leads/', generate_leads),
]