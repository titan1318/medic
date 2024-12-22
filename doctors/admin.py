from django.contrib import admin

from doctors.models import Doctor, DoctorSpeciality


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user',)
    list_filter = ('user',)


@admin.register(DoctorSpeciality)
class DoctorSpecialityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
