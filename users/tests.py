from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserAPITestCase(APITestCase):
    """Тесты для проверки CRUD пользователя"""

    def setUp(self) -> None:
        self.user = User.objects.create(email="test1@mail.com", password="1111", tg_chat_id="8647545387")
        self.client.force_authenticate(user=self.user)

    def test_user_create(self) -> None:
        """Проверка регистрации пользователя"""
        url = reverse("users:user-list")
        data = {
            "email": "test2@mail.com",
            "password": "1111",
            "tg_chat_id": "7657548877",
        }

        response = self.client.post(url, data)
        result_data = response.json()
        expected_data = {
            "id": result_data.get("id"),
            "first_name": "",
            "last_name": "",
            "email": data.get("email"),
            "tg_chat_id": data.get("tg_chat_id"),
        }

        # проверка статус кода
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # проверка созданных данных пользователя
        self.assertEqual(result_data, expected_data)
        # проверка количества созданных пользователей
        self.assertEqual(User.objects.all().count(), 2)

    def test_user_retrieve(self) -> None:
        """Проверка детального просмотра пользователя"""
        user = self.user
        url = reverse("users:user-detail", args=(self.user.pk,))

        response = self.client.get(url)

        result_data = response.json()
        expected_data = {
            "id": user.pk,
            "first_name": "",
            "last_name": "",
            "email": user.email,
            "tg_chat_id": user.tg_chat_id,
        }

        # проверка статус кода
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # проверка детального просмотра пользователя
        self.assertEqual(result_data, expected_data)

    def test_user_update(self) -> None:
        """Проверка обновления пользователя"""
        url = reverse("users:user-detail", args=(self.user.pk,))
        user = self.user
        data = {
            "email": "test2@mail.com",
        }

        response = self.client.patch(url, data)

        result_data = response.json()
        expected_data = {
            "id": user.pk,
            "first_name": "",
            "last_name": "",
            "email": data.get("email"),
            "tg_chat_id": user.tg_chat_id,
        }

        # проверка статус кода
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # проверка обновления названия пользователя
        self.assertEqual(result_data, expected_data)

    def test_user_delete(self) -> None:
        """Проверка удаления пользователя"""
        url = reverse("users:user-detail", args=(self.user.pk,))

        response = self.client.delete(url)

        # проверка статус кода
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # проверка удаления пользователя
        self.assertEqual(User.objects.all().count(), 0)

    def test_user_list(self) -> None:
        """Проверка вывода списка пользователей"""
        url = reverse("users:user-list")
        user = self.user

        response = self.client.get(url)

        result_data = response.json()
        expected_data = [
            {
                "id": user.pk,
                "first_name": "",
                "email": user.email,
            }
        ]

        # проверка статус кода
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # проверка созданных данных пользователя
        self.assertEqual(result_data, expected_data)
