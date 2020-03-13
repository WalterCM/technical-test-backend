from src.utils import serializers
from src.tests.base import TestCase
from src import models


class ModelSerializerTests(TestCase):
    MODELS = [models.User]
    payload = {
        'username': 'test_user',
        'password': '123456'
    }

    class TestUserSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.User
            fields = '__all__'

    def setUp(self):
        super().setUp()
        self.user = models.User.objects.create_user(**self.payload)

    def test_get_all_fields(self):
        serializer = self.TestUserSerializer(self.user)
        fields = serializer.get_fields()

        self.assertIn('username', fields)
        self.assertIn('password', fields)

    def test_get_some_fields(self):
        self.TestUserSerializer.Meta.fields = ('username',)

        serializer = self.TestUserSerializer(self.user)
        fields = serializer.get_fields()

        self.assertIn('username', fields)
        self.assertNotIn('password', fields)

    def test_get_serialized_data(self):
        """Testea que el serializer devuelva la data serializada"""
        serializer = self.TestUserSerializer(self.user)

        self.assertEqual(
            serializer.data.get('username'),
            self.payload.get('username')
        )

    def test_create_instance(self):
        """Testea que el serializer pueda crear un elemento"""
        payload = self.payload.copy()
        payload['username'] = 'new_user'

        serializer = self.TestUserSerializer(data=payload)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        query = models.User.select().where(
            models.User.username == payload.get('username')
        )
        self.assertTrue(query.exists())

    def test_update_instance(self):
        """Testea que el serializer pueda actualizar un elemento"""
        new_username = 'new_username'
        serializer = self.TestUserSerializer(
            self.user,
            data={'username': new_username}
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        self.assertEqual(user.username, new_username)

    def test_list_instances(self):
        """Testea que el serializer pueda listar elementos de un queryset"""
        self.user = models.User.objects.create_user(
            username='second_user',
            password='123456'
        )

        users = models.User.select()

        serializer = self.TestUserSerializer(users, many=True)

        self.assertTrue(len(serializer.data), 2)
