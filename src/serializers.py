from src import models
from src.utils import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ('username', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return models.User.objects.create_user(**validated_data)
