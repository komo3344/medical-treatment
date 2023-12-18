from django.urls import path
from . import views

urlpatterns = [
    path("request", views.TreatmentRequestAPI.as_view()),
    path("<int:pk>/accept", views.TreatmentRequestAcceptAPI.as_view()),
]
