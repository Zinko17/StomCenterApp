from rest_framework import serializers
from .models import *


class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = ['id', 'name']


class DoctorDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorDay
        fields = ['id', 'day']


class DoctorDayDisplaySerializer(serializers.ModelSerializer):
    doctor = serializers.StringRelatedField()
    day = serializers.StringRelatedField()

    class Meta:
        model = DoctorDay
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['day', 'doctor']


class OrderDisplaySerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField()
    day = serializers.StringRelatedField()
    doctor = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = '__all__'


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'groups']


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
