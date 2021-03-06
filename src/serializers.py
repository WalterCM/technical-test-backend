import jwt
import time

from marshmallow import ValidationError, fields, Schema

from src import conf
from src import models
from src.utils import serializers


class TokenSerializer(serializers.ModelSerializer):
    username = fields.Str()
    password = fields.Str()

    class Meta:
        fields = ('username', 'password')

    def validate_password(self, password):
        if len(password) < 6:
            raise ValidationError('Password has a min length of 6 characters')

        return password

    def validate(self, attrs):
        username = attrs.get('username')
        user = models.User.get_or_none(models.User.username == username)
        if not user:
            raise ValidationError('User with that username does not exist')

        password = attrs.get('password')
        if not user.check_password(password):
            raise ValidationError('Wrong password')

        return attrs

    def create(self, validated_data):
        username = validated_data.pop('username', None)
        user = models.User.get(models.User.username == username)

        payload = {
            'user': user.id,
            'exp': time.time() + conf.JWT.get('expire_offset')
        }

        token = jwt.encode(
            payload,
            conf.JWT.get('secret'),
            conf.JWT.get('algorithm')
        )

        return token

    def to_representation(self, token):
        schema = Schema.from_dict({'token': fields.Str()})()
        return schema.dump({'token': token})


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

        return username

    def validate_password(self, password):
        if len(password) < 6:
            raise ValidationError('Password has a min length of 6 characters')

        return password

    def create(self, validated_data):
        return models.User.objects.create_user(**validated_data)


class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Note
        fields = ('id', 'title', 'body', 'created_at', 'last_edited', 'user')
        extra_kwargs = {
            'id': {'read_only': True},
            'title': {'required': False},
            'body': {'required': False},
            'created_at': {'read_only': True},
            'last_edited': {'read_only': True},
            'user': {'read_only': True}
        }

    def create(self, validated_data):
        user = self.context.get('user')
        note = user.create_new_note(**validated_data)

        return note
