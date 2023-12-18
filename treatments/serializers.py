from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from doctors.models import Doctor, BusinessHours
from doctors.serializers import DoctorSerializer
from patients.models import Patient
from patients.serializers import PatientSerializer
from treatments.models import Treatment
from utils.converts import get_day_of_week_from_string


class TreatmentRequestInputSerializer(serializers.Serializer):
    doctor_id = serializers.IntegerField(required=True)
    patient_id = serializers.IntegerField(required=True)
    desired_date = serializers.CharField(required=True)

    def validate_doctor_id(self, doctor_id):
        if not Doctor.objects.filter(id=doctor_id).exists():
            raise ValidationError("존재하지 않는 doctor_id 입니다.")

    def validate_patient_id(self, patient_id):
        if not Patient.objects.filter(id=patient_id).exists():
            raise ValidationError("존재하지 않는 patient_id 입니다.")


class TreatmentRequestOutputSerializer(serializers.Serializer):
    doctor_name = serializers.CharField()
    patient_name = serializers.CharField()
    desired_date = serializers.CharField()
    expired_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M')


class TreatmentRequestSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name')
    desired_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    expired_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = Treatment
        fields = [
            'id',
            'patient_name',
            'desired_date',
            'expired_date',
            'is_accept',
        ]
