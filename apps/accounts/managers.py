from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        auth_provider = extra_fields.get("auth_provider", "email")

        user = self.model(
            email=email,
            name=name,
            **extra_fields
        )

        if auth_provider == "email":
            if not password:
                raise ValueError("Password is required for email users")
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)
        extra_fields.setdefault("auth_provider", "email")

        if not password:
            raise ValueError("Superusers must have a password")

        return self.create_user(email, name, password, **extra_fields)
