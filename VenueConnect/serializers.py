from rest_framework import serializers


class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)

    def validate(self, data):
        if 'username' not in data or 'email' not in data or 'password' not in data:
            raise serializers.ValidationError("Username, email and password are required")
        return data
