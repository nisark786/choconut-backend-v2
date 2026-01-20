from rest_framework import serializers


class OTPStartSerializer(serializers.Serializer):
    email = serializers.CharField()
    purpose = serializers.ChoiceField(choices=["signup", "login", "reset"])


class OTPVerifySerializer(serializers.Serializer):
    email = serializers.CharField()
    otp = serializers.CharField(max_length=6)
    purpose = serializers.ChoiceField(choices=["signup", "login", "reset"])
