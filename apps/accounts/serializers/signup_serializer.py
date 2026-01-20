from rest_framework import serializers
from apps.accounts.models.user_model import UserModel

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = UserModel
        fields = ["name", "email", "password"]
        extra_kwargs = {
            'email': {'validators': []} 
        }

    def validate_email(self, value):
        value = value.lower().strip()
        user = UserModel.objects.filter(email=value).first()
        
        if user:
            if user.is_active:
                raise serializers.ValidationError("User already exists. Please login.")
            else:
                
                self.existing_user = user 
        return value

    def create(self, validated_data):
  
        password = validated_data.pop("password")
        
   
        user = getattr(self, 'existing_user', None)
        
        if user:
          
            user.name = validated_data.get("name", user.name)
            user.email = validated_data.get("email", user.email)
        else:
    
            user = UserModel(**validated_data)

        user.set_password(password)
        
       
        user.is_active = False
        user.is_verified = False
        user.save()
        return user