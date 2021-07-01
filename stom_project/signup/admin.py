from django.contrib import admin
from .models import *


class DayAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Day, DayAdmin)


class DayDoctorAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'day']


admin.site.register(DoctorDay, DayDoctorAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['client', 'doctor', 'day', 'date_created']
    readonly_fields = ['date_created']


admin.site.register(Order, OrderAdmin)
