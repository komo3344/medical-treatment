from django.db.models import Q
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from doctors.models import Doctor, BusinessHours
from patients.models import Patient
from treatments.models import Treatment
from treatments.serializers import TreatmentRequestInputSerializer, TreatmentRequestOutputSerializer, \
    TreatmentRequestSerializer
from treatments.servicecs import TreatmentService
from utils.converts import get_day_of_week_from_string


@extend_schema(
    tags=['진료'], summary='진료 요청',
    request=TreatmentRequestInputSerializer,
    examples=[
        OpenApiExample(
            name="진료 요청 예시",
            summary="id 11인 환자가 id 10인 의사에게 2023년 12월 15일 오전 10시에 진료 요청",
            value={
                "doctor_id": 10,
                "patient_id": 11,
                "desired_date": "2023-12-15 10:00",
            },
        ),
    ],
    responses={201: TreatmentRequestOutputSerializer})
class TreatmentRequestAPI(APIView):
    def post(self, request, *args, **kwargs):
        serializer = TreatmentRequestInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        doctor_id = request.data['doctor_id']

        date, time = request.data['desired_date'].split(" ")[0], request.data['desired_date'].split(" ")[1]
        week_of_day = get_day_of_week_from_string(request.data['desired_date'])

        desired_date = request.data['desired_date']
        service = TreatmentService(
            doctor_id=doctor_id,
            patient_id=request.data['patient_id'],
            desired_date=desired_date
        )
        is_business_hours = BusinessHours.objects.filter(
            Q(doctor_id=doctor_id) &
            Q(day=week_of_day, opening_time__lte=time, closing_time__gte=time, is_working_day=True) &
            ~Q(start_lunch_time__lte=time, end_lunch_time__gte=time)
        ).exists()
        if not is_business_hours:
            desired_date = "의사의 영업 시간이 아닙니다."

        treatment_model = service.create_treatment_request()

        output_data = {
            'id': treatment_model.id,
            'doctor_name': Doctor.objects.get(id=request.data['doctor_id']).name,
            'patient_name': Patient.objects.get(id=request.data['patient_id']).name,
            'desired_date': desired_date,
            'expired_date': service.get_expired_datetime()
        }

        output_serializer = TreatmentRequestOutputSerializer(data=output_data)
        output_serializer.is_valid(raise_exception=True)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=['진료'], summary='진료 요청 수락', responses=TreatmentRequestSerializer)
class TreatmentRequestAcceptAPI(APIView):
    def post(self, request, *args, **kwargs):
        now = timezone.now()
        treatment = get_object_or_404(Treatment, pk=self.kwargs['pk'])

        if now > treatment.expired_date:
            raise ValidationError('만료시간이 지나 요청을 수락할 수 없습니다.')

        treatment.is_accept = True
        treatment.save(update_fields=['is_accept'])
        serializer = TreatmentRequestSerializer(treatment)

        return Response(serializer.data, status=status.HTTP_200_OK)
