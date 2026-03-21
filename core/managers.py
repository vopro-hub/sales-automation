from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, tenant=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        if not tenant:
            raise ValueError("Tenant is required")

        email = self.normalize_email(email)
        user = self.model(email=email, tenant=tenant, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, tenant=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not tenant:
            raise ValueError("Superuser must belong to a tenant")

        return self.create_user(email, password, tenant=tenant, **extra_fields)
