from rest_framework import serializers
from django.contrib.auth.models import User


# TODO: This is placeholder, rethink if we need this or  builtin UserSerializer
# from django will be enough
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # Use Django's built-in create_user to hash password etc.
        return User.objects.create_user(**validated_data)