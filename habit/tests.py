from datetime import datetime

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from habit.models import Habit, Location
from users.models import User


class HabitAPITestCase(APITestCase):

    def setUp(self) -> None:
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

    def test_habit_create(self) -> None:
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

    def test_habit_retrieve(self) -> None:
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

    def test_habit_update(self) -> None:
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

    def test_habit_delete(self) -> None:
        """Проверка удаления привычки"""
        url = reverse("habit:habit-detail", args=(self.habit.pk,))

        response = self.client.delete(url)

        # проверка статус кода
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # проверка удаления привычки
        self.assertEqual(Habit.objects.all().count(), 0)

    def test_habit_list(self) -> None:
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
        # проверка списка привычек
        self.assertEqual(result_data, expected_data)

    def test_published_habit_list(self) -> None:
        """Проверка вывода списка публичных привычек"""
        habit = Habit.objects.create(
            owner=self.user,
            location=self.location,
            time="18:00:25",
            action="Тестовое действие 1",
            is_pleasant=True,
            related_habit=None,
            period="two_days",
            reward="Тестовое вознаграждение 1",
            completion_time=100,
            is_published=True,
        )
        url = reverse("habit:publish-habit-list")

        response = self.client.get(url)

        result_data = response.json()
        expected_data = [
            {
                "id": habit.pk,
                "action": habit.action,
                "is_pleasant": habit.is_pleasant,
                "completion_time": habit.completion_time,
                "is_published": habit.is_published,
            },
        ]

        # проверка статус кода
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # проверка списка публичных привычек
        self.assertEqual(result_data, expected_data)


class LocationAPITestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(email="test@gmail.com")
        self.location = Location.objects.create(
            name="Тестовая локация 1",
            address="Тестовый адрес локации 1",
            description="Тестовый описание локации 1",
        )
        self.client.force_authenticate(user=self.user)

    @staticmethod
    def formater_iso(obj: datetime) -> str:
        """Форматирует объект даты в строку ISO 8601"""
        return timezone.localtime(obj).isoformat()

    def test_location_create(self) -> None:
        """Проверка создания локации"""
        url = reverse("habit:location-list")
        data = {
            "name": "Тестовая локация 2",
            "address": "Тестовый адрес локации 2",
            "description": "Тестовый описание локации 2",
        }

        response = self.client.post(url, data)
        result_data = response.json()
        expected_data = {
            "id": 2,
            "name": data.get("name"),
            "address": data.get("address"),
            "description": data.get("description"),
            "created_at": result_data.get("created_at"),
        }

        # проверка статус кода
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # проверка созданных данных локации
        self.assertEqual(result_data, expected_data)
        # проверка количества созданных локации
        self.assertEqual(Location.objects.all().count(), 2)

    def test_location_retrieve(self) -> None:
        """Проверка детального просмотра локации"""
        location = self.location
        url = reverse("habit:location-detail", args=(location.pk,))

        response = self.client.get(url)

        result_data = response.json()
        expected_data = {
            "id": location.pk,
            "name": location.name,
            "address": location.address,
            "description": location.description,
            "created_at": self.formater_iso(location.created_at),
        }

        # проверка статус кода
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # проверка детального просмотра локации
        self.assertEqual(result_data, expected_data)

    def test_location_update(self) -> None:
        """Проверка обновления локации"""
        location = self.location
        url = reverse("habit:location-detail", args=(location.pk,))
        data = {
            "name": "Тестовая локация 1.1",
            "address": "Тестовый адрес локации 1.1",
        }

        response = self.client.patch(url, data)

        result_data = response.json()
        expected_data = {
            "id": location.pk,
            "name": data.get("name"),
            "address": data.get("address"),
            "description": location.description,
            "created_at": self.formater_iso(location.created_at),
        }

        # проверка статус кода
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # проверка обновления названия локации
        self.assertEqual(result_data, expected_data)

    def test_location_delete(self) -> None:
        """Проверка удаления локации"""
        url = reverse("habit:location-detail", args=(self.location.pk,))

        response = self.client.delete(url)

        # проверка статус кода
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # проверка удаления локации
        self.assertEqual(Location.objects.all().count(), 0)

    def test_location_list(self) -> None:
        """Проверка вывода списка локаций"""
        location = self.location
        url = reverse("habit:location-list")

        response = self.client.get(url)

        result_data = response.json()
        expected_data = [
            {
                "id": location.pk,
                "name": location.name,
                "address": location.address,
                "description": location.description,
                "created_at": self.formater_iso(location.created_at),
            }
        ]

        # проверка статус кода
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # проверка списка локаций
        self.assertEqual(result_data, expected_data)
