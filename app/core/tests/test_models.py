from django.test import TestCase
from django.contrib.auth import get_user_model
# ? https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#referencing-the-user-model  # noqa: E501
# noqa: E501 is used to suppress error E501 i.e., character > 79


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
