"""
All Serializers are here
"""
import re
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Model Serializer to show details of all users
    """
    class Meta:
        """
        Model Mata Class
        """
        model = User
        fields = (
            'email', 'username', 'phone_number', 'first_name', 'last_name'
        )

class RegisterSerializer(UserSerializer):
    """
    Registration Serializer
    """
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta(UserSerializer.Meta):
        """
        Model Meta class
        """
        fields = UserSerializer.Meta.fields + ('password', 'password2')
        extra_kwargs = {
            'phone_number': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': 'password field didn\'t metch'})
        return super().validate(attrs)

    def validate_username(self, username):
        """
        validate username
        """
        if not re.match(r"^[A-Za-z0-9]*$", username):
            raise serializers.ValidationError(
                'username should only contain letters and numbers')
        return username

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user
