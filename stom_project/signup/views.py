from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .serializers import *
from .permissions import IsSuperUser, DoctorDayPermission


class DayViewSet(ViewSet):
    serializer_class = DaySerializer
    permission_classes = [IsSuperUser]

    def list(self, request):
        days = Day.objects.all()
        serializer = self.serializer_class(days, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

    def retrieve(self, request, day_id):
        day = Day.objects.get(id=day_id)
        serializer = self.serializer_class(day)
        return Response(serializer.data, status=200)

    def update(self, request, day_id):
        day = Day.objects.get(id=day_id)
        serializer = self.serializer_class(day, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=202)

    def destroy(self, request, day_id):
        day = Day.objects.get(id=day_id)
        day.delete()
        return Response(status=204)


class DoctorDayView(ViewSet):
    serializer_class = DoctorDaySerializer
    permission_classes = [DoctorDayPermission]

    def list(self, request):
        doctor_days = DoctorDay.objects.filter(doctor=request.user)
        serializer = DoctorDaySerializer(doctor_days, many=True)
        return Response(serializer.data, status=200)

    def create(self, request, day_id):
        day = Day.objects.get(id=day_id)
        work_day = DoctorDay.objects.create(doctor=request.user, day=day)
        serializer = self.serializer_class(work_day)
        return Response(serializer.data, status=201)

    def update(self, request, doctor_day_id):
        work_day = DoctorDay.objects.get(id=doctor_day_id)
        serializer = DoctorDaySerializer(work_day, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=202)

    def retrieve(self, request, doctor_day_id):
        work_day = DoctorDay.objects.get(id=doctor_day_id)
        serializer = DoctorDaySerializer(work_day)
        return Response(serializer.data, status=200)
