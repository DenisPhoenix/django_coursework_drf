from rest_framework.routers import SimpleRouter

from habit.views import HabitViewSet, LocationViewSet

router = SimpleRouter()
router.register(r"locations", LocationViewSet, "location")
router.register(r"habits", HabitViewSet, "habit")

urlpatterns = router.urls
