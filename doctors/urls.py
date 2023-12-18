from django.urls import path
from . import views
urlpatterns = [
    path("", views.DoctorSearchAPI.as_view()),
    path("<int:pk>/treatment-request", views.TreatmentRequestListAPI.as_view())

]
