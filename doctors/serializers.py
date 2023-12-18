from rest_framework import serializers

from doctors.models import Doctor
from hospitals.serializers import HospitalSerializer, MedicalDepartmentSerializer


class DoctorSerializer(serializers.ModelSerializer):
    hospital = HospitalSerializer()
    medial_department = MedicalDepartmentSerializer(many=True, read_only=True)

    class Meta:
        model = Doctor
        fields = [
            'id',
            'name',
            'hospital',
            'medial_department',
        ]
