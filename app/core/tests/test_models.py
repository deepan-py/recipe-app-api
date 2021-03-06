from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch
from .. import models
# ? https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#referencing-the-user-model  # noqa: E501
# noqa: E501 is used to suppress error E501 i.e., character > 79


def sample_user(email='test@test.com', password='test@123'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successfully(self):
        """Test Creating new user with an email is successful"""
        email = "test@test.com"
        password = "Testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        # user.check_password(password) Returns True if the given raw string \
        # is the correct password for the user. \
        # (This takes care of the password hashing in making the comparison.)
        # ? https://docs.djangoproject.com/en/3.2/ref/contrib/auth/#django.contrib.auth.models.User.check_password  # noqa: E501
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email for new user is normalized"""
        email = "test@TEST.com"
        user = get_user_model().objects.create_user(email, "test123")
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test Creating with no email raise error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating new superuser"""
        user = get_user_model().objects.create_superuser(
            "test@test.com", "test123"
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """"Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='vegan tag'
        )
        self.assertEqual(str(tag), tag.name)

    def test_intgredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='customer'
        )
        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title="Steak and mushroom sauce",
            time_minutes=5,
            price=5.00
        )
        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'my_img.jpg')
        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
