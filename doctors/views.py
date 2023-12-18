from datetime import datetime

from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from doctors.models import Doctor
from doctors.serializers import DoctorSerializer
from treatments.models import Treatment
from treatments.serializers import TreatmentRequestSerializer
from utils.converts import get_day_of_week_from_string


@extend_schema(
    tags=['의사'], summary='의사 검색(문자열, 날짜와 시간)',
    parameters=[
        OpenApiParameter(
            name="query",
            type=str,
            description="문자열로 검색합니다.",
            required=False,
            ),
        OpenApiParameter(
            name="datetime",
            type=str,
            description="특정 날짜와 시간으로 검색합니다. (%Y-%m-%d %H:%M) 형식을 준수 해야합니다. ex) 2023-12-15 10:30",
            required=False,
        ),
    ],
    responses=DoctorSerializer
)
class DoctorSearchAPI(APIView):
    def get(self, request, *args, **kwargs):
        query = self.request.query_params.get('query', None)
        date_time = self.request.query_params.get('datetime', None)

        if not query and not date_time:
            return Response(status=status.HTTP_204_NO_CONTENT)

        if query:
            query_tokens = query.split(" ")
            query_filters = Q()
            for token in query_tokens:
                if len(query_tokens) > 1:
                    query_filters &= Q(name__icontains=token) | Q(medial_department__name__icontains=token) | Q(
                        hospital__name__icontains=token)
                else:
                    query_filters |= Q(name__icontains=token) | Q(medial_department__name__icontains=token) | Q(
                        hospital__name__icontains=token)
            doctors = Doctor.objects.filter(query_filters).distinct()

        if date_time:
            datetime_split = date_time.split(" ")
            date, time = datetime_split[0], datetime_split[1]

            day_of_week = get_day_of_week_from_string(date_time)
            time_from_str = datetime.strptime(time, "%H:%M").time()

            doctors = Doctor.objects.filter(
                Q(business_hours__day=day_of_week) &
                Q(business_hours__opening_time__lte=time_from_str, business_hours__closing_time__gte=time_from_str) &
                ~Q(business_hours__start_lunch_time__lte=time_from_str, business_hours__end_lunch_time__gte=time_from_str)
            ).distinct()

        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=['의사'], summary='해당 의사의 진료요청 검색', responses=TreatmentRequestSerializer)
class TreatmentRequestListAPI(APIView):
    def get(self, request, *args, **kwargs):
        doctor = get_object_or_404(Doctor, pk=self.kwargs['pk'])
        treatments = Treatment.objects.filter(doctor=doctor, is_accept=False)
        serializer = TreatmentRequestSerializer(treatments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
