from django.db import models

from common import models as common_models


class Treatment(common_models.DateTimeModel):
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.CASCADE)
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE)
    desired_date = models.DateTimeField(help_text="희망 날짜")
    expired_date = models.DateTimeField(help_text="만료 날짜", null=True, blank=True)
    is_accept = models.BooleanField(default=False)

    def __str__(self):
        return f"doctor: {self.doctor.name} patient: {self.patient.name}"

    class Meta:
        db_table = "treatment"
        verbose_name_plural = "진료"
