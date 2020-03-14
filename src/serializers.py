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
