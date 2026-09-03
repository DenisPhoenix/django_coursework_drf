from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habit.models import Habit, Location
from users.models import User


class HabitAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@gmail.com")
        self.location = Location.objects.create(name="test_place")
        self.habit = Habit.objects.create(
            owner=self.user,
            location=self.location,
            time="18:00:25",
            action="Тестовое действие 1",
            is_pleasant=True,
            related_habit=None,
            period="two_days",
            reward="Тестовое вознаграждение 1",
            completion_time=100,
            is_published=False,
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_create(self):
        """Проверка создания привычки"""
        url = reverse("habit:habit-list")
        data = {
            "location": self.location.pk,
            "time": "12:00:12",
            "action": "Тестовое действие 2",
            "is_pleasant": True,
            "related_habit": 1,
            "period": "daily",
            "completion_time": 80,
            "is_published": True,
        }

        response = self.client.post(url, data)
        result_data = response.json()
        expected_data = {
            "id": 2,
            "owner": self.user.pk,
            "location": self.location.pk,
            "time": data.get("time"),
            "action": data.get("action"),
            "is_pleasant": data.get("is_pleasant"),
            "related_habit": data.get("related_habit"),
            "period": data.get("period"),
            "reward": data.get("reward"),
            "completion_time": data.get("completion_time"),
            "is_published": data.get("is_published"),
        }

        # проверка статус кода
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # проверка созданных данных привычки
        self.assertEqual(result_data, expected_data)
        # проверка количества созданных привычки
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_retrieve(self):
        """Проверка детального просмотра привычки"""
        habit = self.habit
        url = reverse("habit:habit-detail", args=(habit.pk,))

        response = self.client.get(url)

        result_data = response.json()
        expected_data = {
            "id": habit.pk,
            "owner": self.user.pk,
            "location": self.location.pk,
            "time": habit.time,
            "action": habit.action,
            "is_pleasant": habit.is_pleasant,
            "related_habit": habit.related_habit,
            "period": habit.period,
            "reward": habit.reward,
            "completion_time": habit.completion_time,
            "is_published": habit.is_published,
        }

        # проверка статус кода
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # проверка детального просмотра привычки
        self.assertEqual(result_data, expected_data)

    def test_habit_update(self):
        """Проверка обновления привычки"""
        habit = self.habit
        url = reverse("habit:habit-detail", args=(habit.pk,))
        data = {
            "time": "18:01:25",
            "action": "Тестовое действие 1",
        }

        response = self.client.patch(url, data)

        result_data = response.json()
        expected_data = {
            "id": habit.pk,
            "owner": self.user.pk,
            "location": self.location.pk,
            "time": data.get("time"),
            "action": data.get("action"),
            "is_pleasant": habit.is_pleasant,
            "related_habit": habit.related_habit,
            "period": habit.period,
            "reward": habit.reward,
            "completion_time": habit.completion_time,
            "is_published": habit.is_published,
        }

        # проверка статус кода
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # проверка обновления названия привычки
        self.assertEqual(result_data, expected_data)

    def test_habit_delete(self):
        """Проверка удаления привычки"""
        url = reverse("habit:habit-detail", args=(self.habit.pk,))

        response = self.client.delete(url)

        # проверка статус кода
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # проверка удаления привычки
        self.assertEqual(Habit.objects.all().count(), 0)

    def test_habit_list(self):
        """Проверка вывода списка привычек"""
        habit = self.habit
        url = reverse("habit:habit-list")

        response = self.client.get(url)

        result_data = response.json()
        expected_data = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": habit.pk,
                    "action": habit.action,
                    "is_pleasant": habit.is_pleasant,
                    "completion_time": habit.completion_time,
                    "is_published": habit.is_published,
                },
            ],
        }

        # проверка статус кода
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # проверка созданных данных привычки
        self.assertEqual(result_data, expected_data)
