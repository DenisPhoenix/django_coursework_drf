from typing import Union

from django.urls import URLPattern, URLResolver, path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserViewSet

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"", UserViewSet, basename="user")

urlpatterns: list[Union[URLPattern, URLResolver]] = [
    path("token/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="token_refresh"),
]

urlpatterns += router.urls
