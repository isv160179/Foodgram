from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework.fields import SerializerMethodField

from foodgram.serializers import RecipeSerializer
from recipes.models import Recipe

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField(read_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('is_subscribed',)

    # class Meta(UserSerializer.Meta):
    #     fields = (
    #         'email',
    #         'id',
    #         'username',
    #         'first_name',
    #         'last_name',
    #         'is_subscribed'
    #     )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return (
                user.is_authenticated
                and obj.subscribing.filter(user=user).exists()
        )


class SubscribeSerializer(CustomUserSerializer):
    recipes = SerializerMethodField(method_name='get_recipes')
    recipes_count = SerializerMethodField(method_name='get_recipes_count')

    class Meta(CustomUserSerializer.Meta):
        fields = CustomUserSerializer.Meta.fields + (
            'recipes',
            'recipes_count',
        )

    def get_recipes(self, obj):
        author_recipes = Recipe.objects.filter(author=obj)

        if 'recipes_limit' in self.context.get('request').GET:
            recipes_limit = self.context.get('request').GET['recipes_limit']
            author_recipes = author_recipes[:int(recipes_limit)]

        if author_recipes:
            serializer = RecipeSerializer(
                author_recipes,
                context={'request': self.context.get('request')},
                many=True
            )
            return serializer.data

        return RecipeSerializer(many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()
