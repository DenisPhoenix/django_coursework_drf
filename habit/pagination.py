from rest_framework.pagination import PageNumberPagination


class HabitPaginator(PageNumberPagination):
    """Ограничение вывода объектов"""

    page_size = 5
