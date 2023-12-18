from django.urls import path, include

urlpatterns = [
    path("doctors/", include('doctors.urls')),
    path("treatments/", include('treatments.urls'))
]
