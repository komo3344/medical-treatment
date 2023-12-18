from rest_framework import serializers

from hospitals.models import Hospital, MedicalDepartment


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['name']


class MedicalDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalDepartment
        fields = ['name']
