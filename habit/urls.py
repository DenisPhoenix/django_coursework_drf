from django.urls import path
from rest_framework.routers import SimpleRouter

from habit.apps import HabitConfig
from habit.views import HabitViewSet, LocationViewSet, PublishedHabit

app_name = HabitConfig.name

router = SimpleRouter()
router.register(r"locations", LocationViewSet, "location")
router.register(r"habits", HabitViewSet, "habit")

urlpatterns = [path("publish/", PublishedHabit.as_view(), name="publish-list")]

urlpatterns += router.urls
