from src import models
from src.tests.base import TestCase


class ModelTests(TestCase):
    MODELS = [models.User]
    payload = {
        'username': 'test_user',
        'password': 'as5d1qg5q61w5d'
    }

    def test_create_user(self):
        """Testea que se pueda crear un usuario usando una funcion de modelo"""
        user = models.User.objects.create_user(**self.payload)

        self.assertEqual(user.username, self.payload.get('username'))
        self.assertTrue(user.check_password(self.payload.get('password')))

    def test_create_user_no_username(self):
        """Testea que no se pueda crear usuario sin username"""
        payload = self.payload.copy()
        del payload['username']

        with self.assertRaises(ValueError):
            models.User.objects.create_user(**payload)

    def test_create_user_no_password(self):
        """Testea que no se pueda crear usuario sin password"""
        payload = self.payload.copy()
        del payload['password']

        with self.assertRaises(ValueError):
            models.User.objects.create_user(**payload)

    def test_create_user_weak_password(self):
        """Testea que no se pueda crear un usuario usando un pass debil"""
        payload = self.payload.copy()
        payload['password'] = '123'

        with self.assertRaises(ValueError):
            models.User.objects.create_user(**payload)
