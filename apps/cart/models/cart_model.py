from django.db import models
from apps.accounts.models.user_model import UserModel



class Cart(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
