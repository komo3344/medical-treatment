from django.contrib import admin

from treatments.models import Treatment


@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'doctor',
        'patient',
        'desired_date',
        'expired_date',
        'is_accept',
    ]

    # 관리자페이지에서 데이터 추가 위해 주석처리
    # readonly_fields = ['doctor', 'patient', 'desired_date', 'expired_date']
