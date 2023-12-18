from django.db import models

from common import models as common_models


class Patient(common_models.DateTimeModel):
    name = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "patients"
        verbose_name_plural = "환자"
