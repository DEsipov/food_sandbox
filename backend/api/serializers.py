from rest_framework import serializers

from core.models import Ingredient, Recipe, IngredientRecipe


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Ingredient."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели IngredientRecipe."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def validate(self, attrs):
        return super().validate(attrs)


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe."""

    ingredients = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'ingredients',)

    def get_ingredients(self, obj):
        ingredients = IngredientRecipe.objects.filter(recipe=obj)
        return IngredientRecipeSerializer(ingredients, many=True).data


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и изменения рецептов."""

    # ingredients = IngredientRecipeSerializer(many=True, read_only=True)
    ingredients = IngredientRecipeSerializer(many=True, read_only=False)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'ingredients', )

    def add_ingredients(self, ingredients, recipe):
        IngredientRecipe.objects.bulk_create([IngredientRecipe(
            recipe=recipe,
            ingredient=ingredient['id'],
            amount=ingredient['amount'],
        ) for ingredient in ingredients])

    # def validate(self, attrs):
    #     return super().validate(attrs)
    #
    def create(self, validated_data):
        # ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        # self.add_ingredients(ingredients, recipe)
        return recipe



