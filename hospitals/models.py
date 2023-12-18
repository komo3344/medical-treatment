from django.db import models

from common import models as common_models


class Hospital(common_models.DateTimeModel):
    name = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "hospital"
        verbose_name_plural = "병원"


class MedicalDepartment(common_models.DateTimeModel):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "medical_department"
        verbose_name_plural = "진료과"
