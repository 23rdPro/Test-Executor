from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['url', 'username', 'password', 'is_active']

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            None,
            validated_data['password']
        )
        return user
