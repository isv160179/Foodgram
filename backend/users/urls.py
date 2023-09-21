from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import CustomTokenCreateView, CustomTokenDestroyView, \
    CustomUserViewSet

app_name = 'users'

router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')
urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path(
        'auth/token/login/',
        CustomTokenCreateView.as_view(),
        name='login'
    ),
    path(
        'auth/token/logout/',
        CustomTokenDestroyView.as_view(),
        name='logout'
    ),
    path('auth/', include('djoser.urls.authtoken')),
]
