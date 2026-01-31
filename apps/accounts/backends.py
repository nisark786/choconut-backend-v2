
from django.contrib.auth.backends import ModelBackend
from apps.accounts.models.user_model import UserModel

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        email = username or kwargs.get('email')
        
        if not email or not password:
            return None
            
        try:
            user = UserModel.objects.get(email=email)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None
        return None