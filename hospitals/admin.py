from django.contrib import admin

from hospitals.models import Hospital, MedicalDepartment


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    pass


@admin.register(MedicalDepartment)
class MedicalDepartmentAdmin(admin.ModelAdmin):
    pass
