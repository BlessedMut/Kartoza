from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.test import TestCase


class TrySecretKeyCheck(TestCase):
    def test_secret_key_length(self):
        SECRET_KEY = settings.SECRET_KEY
        self.assertGreater(len(SECRET_KEY), 50)

    def test_secret_key_strength(self):
        SECRET_KEY = settings.SECRET_KEY
        try:
            is_strong = validate_password(SECRET_KEY)
        except Exception:
            msg = f'Weak Secret Key'
            self.fail(msg)

    def test_create_user(self):
        User = get_user_model()
        try:
            user = User.objects.create_user(username='doe', password='foo')
            self.assertIsNotNone(user.username)
        except Exception:
            msg = "Username cannot be empty"
            self.fail(msg)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(username='doe', email='super@user.com', password='foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            self.assertIsNotNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                username='doe', email='super@user.com', password='foo', is_superuser=False)
