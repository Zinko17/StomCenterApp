from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .serializers import *
from .permissions import IsSuperUser, DoctorDayPermission, ClientPermission,DoctorPermission


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
        return Response(serializer.errors)

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
        return Response(serializer.errors)

    def retrieve(self, request, doctor_day_id):
        work_day = DoctorDay.objects.get(id=doctor_day_id)
        serializer = DoctorDaySerializer(work_day)
        return Response(serializer.data, status=200)


class OrderViewSet(ViewSet):
    permission_classes = [ClientPermission]
    serializer_class = OrderSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        client = request.user
        if serializer.is_valid():
            doctor_id = serializer.data.get('doctor')
            day_id = serializer.data.get('day')
            try:
                work_day = DoctorDay.objects.get(doctor=doctor_id, day=day_id)
                day = Day.objects.get(id=day_id)
                doctor = User.objects.get(id=doctor_id)
                if work_day.status == 'free':
                    order = Order.objects.create(client=client, doctor=doctor, day=day)
                    work_day.status = 'reserved'
                    work_day.save()
                    return Response(serializer.data, status=201)
                return Response('?????? ?????????? ?????? ????????????!', 400)
            except DoctorDay.DoesNotExist:
                return Response('???????? ?? ?????????? ???????? ???? ????????????????!', status=404)
        return Response(serializer.errors, status=400)

    def list(self, request):
        group = request.user.groups.all()[0].name
        user = request.user
        if group == 'client':
            orders = Order.objects.filter(client=user)
        elif group == 'doctor':
            orders = Order.objects.filter(doctor=user)
        serializer = OrderDisplaySerializer(orders, many=True)
        return Response(serializer.data)

    def update(self, request, order_id):
        order = Order.objects.get(id=order_id)
        serializer = self.serializer_class(order, data=request.data)
        if serializer.is_valid():
            day_id = request.data.get('day')
            doctor_id = request.data.get('doctor')
            try:
                dd = DoctorDay.objects.get(day=day_id,doctor=doctor_id,status='free')
                dd.status = 'reserved'
                dd.save()
            except DoctorDay.DoesNotExist:
                return Response('???????????? ?? ?????? ???????? ???? ????????????????,???????? ???????? ??????????.')
            serializer.save()
            return Response(serializer.data, status=202)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, order_id):
        order = Order.objects.get(id=order_id)
        serializer = self.serializer_class(order)
        return Response(serializer.data, status=200)

    def destroy(self, request, order_id):
        order = Order.objects.get(id=order_id)
        o_id = order.id
        order.delete()
        return Response(f'{o_id} successfully deleted!', status=204)


class DoctorViewSet(ViewSet):
    permission_classes = [DoctorPermission]
    serializer_class = UserDetailSerializer
    def list(self,request):
        doctors = User.objects.filter(groups__name='doctor')
        serializer = UserListSerializer(doctors, many=True)
        return Response(serializer.data,status=200)

    def retrieve(self,request,d_username):
        doctor = User.objects.get(username=d_username)
        serializer = self.serializer_class(doctor)
        return Response(serializer.data,status=200)

    def update(self,request,d_username):
        doctor = User.objects.get(username=d_username)
        serializer = self.serializer_class(doctor,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=202)
        return Response(serializer.errors,status=400)

    def destroy(self,request,d_username):
        doctor = User.objects.get(username=d_username)
        doctor.delete()
        return Response('Successfully deleted',status=204)

