from src import models
from src.tests.base import TestCase


class UserTests(TestCase):
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


class NoteTests(TestCase):
    MODELS = [models.User, models.Note]
    payload = {
        'title': 'Cosas que me gustan',
        'body': 'Musica\nProgramacion\nFilosofia'
    }

    def setUp(self):
        super().setUp()
        self.user = models.User.objects.create_user(
            username='waltercm',
            password='123456'
        )

    def test_create_new__empty_note(self):
        """Testea que un usuario pueda crear una nueva nota"""
        self.user.create_new_note()

    def tesT_edit_note_title(self):
        """Testea que se pueda editar el titulo de una nota"""
        note = self.user.create_new_note()
        self.assertEqual(note.title, '')

        note.set_title(self.payload.get('title'))
        self.assertEqual(note.title, self.payload.get('title'))

    def test_edit_note_body(self):
        """Testea que se pueda editar el cuerpo de una nota"""
        note = self.user.create_new_note()
        self.assertEqual(note.body, '')

        note.set_body(self.payload.get('body'))
        self.assertEqual(note.body, self.payload.get('body'))

    def test_delete_note(self):
        note = self.user.create_new_note()
        notes = models.Note.select()
        self.assertGreater(len(notes), 0)

        note.delete_instance()
        notes = models.Note.select()
        self.assertEqual(len(notes), 0)
