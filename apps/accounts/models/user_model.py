from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from ..managers import UserManager


class UserModel(AbstractBaseUser, PermissionsMixin):


    AUTH_PROVIDERS = (
    ("email", "Email"),
    ("google", "Google"),
)

    auth_provider = models.CharField(
        max_length=20,
        choices=AUTH_PROVIDERS,
        default="email"
    )

    email = models.EmailField(unique=True, db_index=True)
    name = models.CharField(max_length=150)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_groups",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions",
        blank=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def can_set_password(self):
        return self.auth_provider == "email"


    def __str__(self):
        return self.email or str(self.pk)
