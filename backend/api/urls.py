from django.urls import include, path
from rest_framework import routers

from api.views import (CustomTokenCreateView, CustomUserViewSet,
                       IngredientViewSet, RecipeViewSet, TagViewSet)

app_name = 'api'

router = routers.DefaultRouter()

router.register('users', CustomUserViewSet, basename='users')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path(
        'auth/token/login/',
        CustomTokenCreateView.as_view(),
        name='login'
    ),
    path('auth/', include('djoser.urls.authtoken')),
]
