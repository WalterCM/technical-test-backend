from marshmallow import ValidationError

from src import models
from src.utils import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ('username', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_username(self, username):
        if models.User.select().where(
            models.User.username == username
        ).exists():
            raise ValidationError('Username has to be unique')

    def validate_password(self, password):
        if len(password) < 6:
            raise ValidationError('Password has a min length of 6 characters')

    def create(self, validated_data):
        return models.User.objects.create_user(**validated_data)


class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Note
        fields = ('title', 'body', 'created_at', 'last_edited', 'user')
        extra_kwargs = {
            'created_at': {'read_only': True},
            'last_edited': {'read_only': True},
            'user': {'read_only': True}
        }

    def create(self, validated_data):
        user = models.User.objects.create_user(
            username='temp',
            password='123456'
        )

        note = user.create_new_note(**validated_data)

        return note
