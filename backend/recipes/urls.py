from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipes.views import TagViewSet

router = DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
# router.register(r'ingredients', IngredientViewSet, basename='ingredients')
# router.register(r'recipes', RecipeViewSet, basename='recipes')

app_name = 'recipes'

urlpatterns = [
    path('', include(router.urls)),
]