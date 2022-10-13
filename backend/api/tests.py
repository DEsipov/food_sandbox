from unittest import skip

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Ingredient, IngredientRecipe, Recipe


class IngredientViewSetTestCase(APITestCase):

    def setUp(self) -> None:
        self.ingredient = Ingredient.objects.create(
            name='Salt',
            measurement_unit='pound'
        )

    def check_object(self, data, obj):
        self.assertEqual(data.get('id'), obj.pk)
        self.assertEqual(data.get('name'), obj.name)

    def test_get_list(self):
        url = reverse('api:ingredients-list')

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_detail(self):
        url = reverse('api:ingredients-detail',
                      kwargs={'pk': self.ingredient.pk})

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.check_object(resp.data, self.ingredient)


class RecipeViewSetTestCase(APITestCase):

    def setUp(self) -> None:
        self.ingredient = Ingredient.objects.create(
            name='Salt',
            measurement_unit='pound'
        )

        self.recipe = Recipe.objects.create(
            name='Солянка с мухоморами'
        )

        self.ingredient_recipe = IngredientRecipe.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient,
            amount=7,
        )

        self.url = reverse('api:receipts-list')

    def check_object(self, data, obj):
        self.assertEqual(data.get('id'), obj.pk)
        self.assertEqual(data.get('name'), obj.name)
        ingredients = data.get('ingredients')
        ids = {x.get('id') for x in ingredients}
        expected = list(obj.ingredients.values_list('id', flat=True))
        self.assertEqual(ids, set(expected))

    def test_get_list(self):
        resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.check_object(resp.data[0], self.recipe)

    @skip('TODO')
    def test_create(self):
        data = {
            'name': 'Соль',
            'ingredients': [
                dict(
                    name='сахар',
                    amount=1,
                    measurement_unit='ст'
                ),
            ],
        }

        resp = self.client.post(self.url, data=data)

        # self.assertEqual(resp.status_code, 201)
        print(Recipe.objects.count())
        print(Recipe.objects.last().ingredients.all())
