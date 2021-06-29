from django.urls import path
from .views import *

urlpatterns = [
    path('',DayViewSet.as_view({'get':'list'}))
]