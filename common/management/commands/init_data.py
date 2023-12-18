from datetime import time

from django.core.management import BaseCommand
from doctors.models import Doctor, BusinessHours
from patients.models import Patient
from hospitals.models import Hospital, MedicalDepartment


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not MedicalDepartment.objects.exists():
            MedicalDepartment.objects.bulk_create(
                [
                    MedicalDepartment(name='정형외과'),
                    MedicalDepartment(name='한의학과'),
                    MedicalDepartment(name='일반의'),
                    MedicalDepartment(name='내과'),
                    MedicalDepartment(name='피부과'),
                    MedicalDepartment(name='소아과')
                ]

            )
        if not Hospital.objects.exists():
            Hospital.objects.bulk_create(
                [
                    Hospital(name='메라키병원'),
                    Hospital(name='아무개병원')
                ]
            )

        if not Doctor.objects.exists():
            hospital1 = Hospital.objects.get(name='메라키병원')
            Doctor.objects.bulk_create(
                [
                    Doctor(name='손웅래', hospital=hospital1),
                    Doctor(name='선재원', hospital=hospital1)
                ]
            )
            md1 = MedicalDepartment.objects.get(name="일반의")
            md2 = MedicalDepartment.objects.get(name="정형외과")
            md3 = MedicalDepartment.objects.get(name="내과")
            md4 = MedicalDepartment.objects.get(name="한의학과")

            doctor1 = Doctor.objects.get(name="손웅래")
            doctor1.medial_department.add(md1, md2, md3)

            doctor2 = Doctor.objects.get(name="선재원")
            doctor2.medial_department.add(md1, md4)

            BusinessHours.objects.bulk_create(
                [
                    BusinessHours(doctor=doctor1, day='monday', opening_time=time(9, 0), closing_time=time(19, 0),
                                  start_lunch_time=time(11, 0),
                                  end_lunch_time=time(12, 0)),
                    BusinessHours(doctor=doctor1, day='tuesday', opening_time=time(9, 0), closing_time=time(19, 0),
                                  start_lunch_time=time(11, 0),
                                  end_lunch_time=time(12, 0)),
                    BusinessHours(doctor=doctor1, day='wednesday', opening_time=time(9, 0), closing_time=time(19, 0),
                                  start_lunch_time=time(11, 0),
                                  end_lunch_time=time(12, 0)),
                    BusinessHours(doctor=doctor1, day='thursday', opening_time=time(9, 0), closing_time=time(19, 0),
                                  start_lunch_time=time(11, 0),
                                  end_lunch_time=time(12, 0)),
                    BusinessHours(doctor=doctor1, day='friday', opening_time=time(9, 0), closing_time=time(19, 0),
                                  start_lunch_time=time(11, 0),
                                  end_lunch_time=time(12, 0)),
                    BusinessHours(doctor=doctor1, day='saturday', opening_time=None, closing_time=None,
                                  start_lunch_time=None,
                                  end_lunch_time=None, is_working_day=False),
                    BusinessHours(doctor=doctor1, day='sunday', opening_time=None, closing_time=None,
                                  start_lunch_time=None,
                                  end_lunch_time=None, is_working_day=False),

                    BusinessHours(doctor=doctor2, day='monday', opening_time=time(8, 0), closing_time=time(17, 0),
                                  start_lunch_time=time(12, 0),
                                  end_lunch_time=time(13, 0)),
                    BusinessHours(doctor=doctor2, day='tuesday', opening_time=time(8, 0), closing_time=time(17, 0),
                                  start_lunch_time=time(12, 0),
                                  end_lunch_time=time(13, 0)),
                    BusinessHours(doctor=doctor2, day='wednesday', opening_time=time(8, 0), closing_time=time(17, 0),
                                  start_lunch_time=time(12, 0),
                                  end_lunch_time=time(13, 0)),
                    BusinessHours(doctor=doctor2, day='thursday', opening_time=time(8, 0), closing_time=time(17, 0),
                                  start_lunch_time=time(12, 0),
                                  end_lunch_time=time(13, 0)),
                    BusinessHours(doctor=doctor2, day='friday', opening_time=time(8, 0), closing_time=time(17, 0),
                                  start_lunch_time=time(12, 0),
                                  end_lunch_time=time(13, 0)),
                    BusinessHours(doctor=doctor2, day='saturday', opening_time=time(8, 0), closing_time=time(13, 0),
                                  start_lunch_time=None,
                                  end_lunch_time=None),
                    BusinessHours(doctor=doctor2, day='sunday', opening_time=None, closing_time=None,
                                  start_lunch_time=None,
                                  end_lunch_time=None, is_working_day=False)
                ]
            )
        if not Patient.objects.exists():
            Patient.objects.bulk_create(
                [
                    Patient(name='김환자'),
                    Patient(name='박환자'),
                    Patient(name='이환자')
                ]
            )

        self.stdout.write(self.style.SUCCESS(f'초기 데이터 생성 완료'))
