from django.urls import path
from .views import PubMedFetchView

urlpatterns = [
    path('fetch_papers/', PubMedFetchView.as_view(), name='fetch_papers')
]
