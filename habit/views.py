from rest_framework.viewsets import ModelViewSet

from habit.models import Habit, Location
from habit.serializers import HabitSerializer, LocationSerializer


class LocationViewSet(ModelViewSet):
    """Вьюсет для локаций"""

    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class HabitViewSet(ModelViewSet):
    """Вьюсет для привычки"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
