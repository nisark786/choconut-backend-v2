from rest_framework import serializers
from apps.accounts.models.user_model import UserModel
from rest_framework import serializers



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = UserModel
        fields = ['id', 'name', 'email', 'password', 'is_staff', 'is_active', 'date_joined']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = UserModel(**validated_data)
        if password:
            user.set_password(password)
        user.is_active = False
        user.is_email_verified = False
        user.save()
        return user
