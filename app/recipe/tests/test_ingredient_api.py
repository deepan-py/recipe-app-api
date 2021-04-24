from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from ..serializer import IngredientSerializer
try:
    from ...core.models import Ingredient
except ImportError:
    from core.models import Ingredient

INGREDIENT_URL = reverse('recipe:ingredients-list')
# the 'ingredients-list' the firstpart 'ingredients' \
# is the basename in 'urls.py' the 'list' represents the URL patterns


class PublicIngredintApiTests(TestCase):
    """Test that publically available ingredients API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the ingredient"""
        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTests(TestCase):
    """Test private ingredients API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            'test@123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients_test(self):
        """Test retrieving a list of ingredients"""
        Ingredient.objects.create(user=self.user, name='Kale')
        Ingredient.objects.create(user=self.user, name='Banner')

        res = self.client.get(INGREDIENT_URL)
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test that ingredients for the authenticated user are returened"""
        user2 = get_user_model().objects.create_user(
            'test2@test.com',
            'test@123'
        )
        Ingredient.objects.create(user=user2, name='vinegar')
        ingredient = Ingredient.objects.create(user=self.user, name='Turmeric')
        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_create_ingredient_successfull(self):
        """Test create a new ingredient"""
        payload = {'name': 'Cabage'}
        self.client.post(INGREDIENT_URL, payload)
        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        """Test creating invalid ingredient fails"""
        payload = {'name': ''}
        res = self.client.post(INGREDIENT_URL, payload)
        self.assertEqual(res.status_code,  status.HTTP_400_BAD_REQUEST)
