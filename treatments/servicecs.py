from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404
from django.utils import timezone

from doctors.models import BusinessHours
from treatments.models import Treatment
from utils.converts import get_day_of_week_from_string


class TreatmentService:
    def __init__(self, doctor_id: int, patient_id: int, desired_date: str):
        self.desired_datetime = datetime.strptime(desired_date, '%Y-%m-%d %H:%M')
        self.day_of_week = get_day_of_week_from_string(desired_date)
        self.doctor_id = doctor_id
        self.patient_id = patient_id

    def create_treatment_request(self):
        treatment = Treatment.objects.create(
            doctor_id=self.doctor_id,
            patient_id=self.patient_id,
            desired_date=self.desired_datetime,
            expired_date=timezone.make_aware(self.get_expired_datetime(), timezone.get_current_timezone())
        )

        return treatment

    def get_expired_datetime(self):
        """
        점심시간: 점심시간 끝나는 시간 + 15분
        휴무일: 다음 영업일 + 15분
        나머지: 진료요청 + 20분
        """
        if self.is_holiday():
            return self.get_next_working_datetime() + timedelta(minutes=15)
        elif self.is_lunch_time():
            end_lunch_time = (
                BusinessHours.objects.get(
                    doctor_id=self.doctor_id, day=self.day_of_week, is_working_day=True
                ).end_lunch_time
            )

            end_lunch_datetime = datetime.combine(self.desired_datetime.date(), end_lunch_time)
            return end_lunch_datetime + timedelta(minutes=15)
        else:
            return self.desired_datetime + timedelta(minutes=20)

    def is_lunch_time(self) -> bool:
        try:
            business_hours = BusinessHours.objects.get(doctor_id=self.doctor_id, day=self.day_of_week, is_working_day=True)
        except BusinessHours.DoesNotExist:
            return False

        start_lunch_time, end_lunch_time = business_hours.start_lunch_time, business_hours.end_lunch_time

        return start_lunch_time <= self.desired_datetime.time() <= end_lunch_time

    def is_holiday(self) -> bool:
        is_working_day = BusinessHours.objects.get(doctor_id=self.doctor_id, day=self.day_of_week).is_working_day

        return False if is_working_day else True

    def get_next_working_datetime(self):
        week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        index = week.index(self.day_of_week.lower()) + 1
        rotated_week = week[index:] + week[:index]

        add_date = 0
        for day in rotated_week:
            add_date += 1
            business_hours = BusinessHours.objects.get(doctor_id=self.doctor_id, day=day)
            if business_hours.is_working_day:
                return datetime.combine(self.desired_datetime.date() + timedelta(days=add_date), business_hours.opening_time)

    def accept_treatment_request(self, treatment_id):
        treatment = get_object_or_404(Treatment, pk=treatment_id)
        if treatment.expired_date <= timezone.now():
            pass

        treatment.is_accept = True
        treatment.save(update_fields=['is_accept'])
