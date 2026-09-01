from rest_framework.viewsets import ModelViewSet

from habit.models import Habit, Location
from habit.serializers import HabitSerializer, LocationSerializer


class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class HabitViewSet(ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
