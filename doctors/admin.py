from django.contrib import admin

from doctors.models import Doctor, BusinessHours


class BusinessHoursInline(admin.TabularInline):
    model = BusinessHours
    extra = 7
    max_num = 7


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    raw_id_fields = ["hospital"]
    filter_horizontal = ['medial_department']
    inlines = [BusinessHoursInline]
