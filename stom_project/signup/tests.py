from django.urls import reverse
from rest_framework.test import APITestCase
from .models import Day, User
from django.contrib.auth.models import Group


class DayTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='maksim', password='123456')
        self.manager = User.objects.create_user(username='manager', password='123456')
        self.group1 = Group.objects.create(name='doctor')
        self.group2 = Group.objects.create(name='manager')
        self.user.groups.add(self.group1)
        self.manager.groups.add(self.group2)
        self.day = Day.objects.create(name='monday')

    def test_get_day(self):
        self.url = reverse('day')
        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, 200)

    def test_get_day_as_doctor(self):
        self.client.login(username='maksim', password='123456')
        self.url = reverse('day')
        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, 200)

    def test_post_day_anonymous(self):
        self.url = reverse('day')
        data = {'name': 'tuesday'}
        self.response = self.client.post(self.url, data)
        self.assertEqual(self.response.status_code, 403)

    def test_post_day_doctor(self):
        self.client.login(username='maksim', password='123456')
        self.url = reverse('day')
        data = {'name': 'tuesday'}
        self.response = self.client.post(self.url, data)
        self.assertEqual(self.response.status_code, 201)

    def test_put_day_manager(self):
        self.client.login(username='manager', password='123456')
        self.url = reverse('day_detail', args=(self.day.id,))
        data = {'name': 'moooon'}
        self.response = self.client.put(self.url, data)
        self.assertEqual(self.response.status_code, 202)
