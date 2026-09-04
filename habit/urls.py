from typing import Union

from django.urls import URLPattern, URLResolver, path
from rest_framework.routers import SimpleRouter

from habit.apps import HabitConfig
from habit.views import HabitViewSet, LocationViewSet, PublishedHabit

app_name = HabitConfig.name

router = SimpleRouter()
router.register(r"locations", LocationViewSet, "location")
router.register(r"habits", HabitViewSet, "habit")

urlpatterns: list[Union[URLPattern, URLResolver]] = [
    path("publish_habits/", PublishedHabit.as_view(), name="publish-habit-list"),
]

urlpatterns += router.urls
