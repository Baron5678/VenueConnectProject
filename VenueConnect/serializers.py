from rest_framework import serializers

from VenueConnect import validators


class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(validators=[validators.username_validator])
    email = serializers.EmailField()
    password = serializers.CharField(validators=[validators.password_validator])

    def validate(self, data):
        if 'username' not in data or 'email' not in data or 'password' not in data:
            raise serializers.ValidationError("Username, email and password are required")
        return data
