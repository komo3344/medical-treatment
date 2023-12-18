from datetime import time

from django.db import models

from common import models as common_models


class Doctor(common_models.DateTimeModel):
    name = models.CharField(max_length=10)
    hospital = models.ForeignKey('hospitals.Hospital', on_delete=models.CASCADE, related_name="doctors")
    medial_department = models.ManyToManyField('hospitals.MedicalDepartment', related_name="doctors")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "doctors"
        verbose_name_plural = "의사"


class BusinessHours(common_models.DateTimeModel):
    DAY_CHOICES = [
        ('monday', '월요일'),
        ('tuesday', '화요일'),
        ('wednesday', '수요일'),
        ('thursday', '목요일'),
        ('friday', '금요일'),
        ('saturday', '토요일'),
        ('sunday', '일요일'),
    ]
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, related_name="business_hours")
    day = models.CharField(max_length=10, choices=DAY_CHOICES, db_index=True)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)

    start_lunch_time = models.TimeField(default=time(11, 0), null=True, blank=True)
    end_lunch_time = models.TimeField(default=time(12, 0), null=True, blank=True)
    is_working_day = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.day}"
    class Meta:
        db_table = "business_hours"
        verbose_name_plural = "영업 시간"
