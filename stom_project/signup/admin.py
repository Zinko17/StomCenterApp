from django.contrib import admin
from .models import *

class DayAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(Day,DayAdmin)

class DayDoctorAdmin(admin.ModelAdmin):
    list_display = ['doctor','day']
admin.site.register(DoctorDay,DayDoctorAdmin)
