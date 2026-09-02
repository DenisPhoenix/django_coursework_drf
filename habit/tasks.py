from datetime import datetime, timedelta

from celery import shared_task
from django.utils import timezone

from habit.models import Habit
from habit.services import send_telegram_message
from users.models import User


@shared_task
def reminder_about_habit():
    """Отправка напоминания в телеграм бот"""
    now = timezone.now().today().replace(second=0, microsecond=0)
    habits = Habit.objects.filter(time__isnull=False)
    for habit in habits:
        habit_datetime = datetime.combine(now, habit.time)
        date_notification = habit_datetime - timedelta(minutes=10)

        if now == date_notification:
            email = habit.owner.email
            message = f"Ваша привычка {habit.action} начнется в {habit.time}. Не пропустите!"
            user = User.objects.get(email=email)
            if tg_chat_id := user.tg_chat_id:
                send_telegram_message(tg_chat_id, message)
