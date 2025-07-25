from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    Group,
    Permission,
    PermissionsMixin,
)

# from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def get_by_natural_key(self, id_code):
        return self.get(id_code=id_code)

    def create_normal(
        self,
        first_name=None,
        last_name=None,
        user_type="normal",
        email=None,
        password=None,
        phone_number=None,
        active_mode=True,
        **extra_fields,
    ):
        if not first_name:
            raise ValueError("The 'first_name' must be set")
        elif not last_name:
            raise ValueError("The 'last_name' must be set")
        elif not password:
            raise ValueError("The 'password' must be set")
        elif not phone_number:
            raise ValueError("The 'phone_number' must be set")
        elif not email:
            raise ValueError("The 'email' must be set")

        email = self.normalize_email(email)

        if self.model.objects.filter(email=email).exists():
            raise ValueError(f"The 'email' {email} is already taken.")

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            user_type=user_type,
            email=email,
            phone_number=phone_number,
            active_mode=active_mode,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_admin(
        self,
        first_name=None,
        last_name=None,
        user_type="admin",
        email=None,
        password=None,
        phone_number=None,
        active_mode=True,
        **extra_fields,
    ):
        if not first_name:
            raise ValueError("The 'first_name' must be set")
        elif not last_name:
            raise ValueError("The 'last_name' must be set")
        elif not password:
            raise ValueError("The 'password' must be set")
        elif not phone_number:
            raise ValueError("The 'phone_number' must be set")
        elif not email:
            raise ValueError("The 'email' must be set")

        email = self.normalize_email(email)

        if self.model.objects.filter(email=email).exists():
            raise ValueError(f"The 'email' {email} is already taken.")

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            user_type=user_type,
            email=email,
            phone_number=phone_number,
            active_mode=active_mode,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):

    USER_TYPES = [
        ("normal", "Normal"),
        ("admin", "Admin"),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user_type = models.CharField(max_length=50, choices=USER_TYPES, default="normal")
    phone_number = models.PhoneNumberField(unique=True, blank=False, null=False)
    email = models.EmailField(max_length=254, unique=True)
    active_mode = models.BooleanField(default=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        related_name="customuser_set",
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="customuser_set",
        related_query_name="customuser",
    )

    def get_by_natural_key(self, id_code):
        return self.get(id_code=id_code)

    objects = CustomUserManager()
    USERNAME_FIELD = "id"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Order(models.Model):
    title = models.CharField(
        blank=False,
        null=False,
        max_length=100,
    )
    owner = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name="orders",
        null=False,
        blank=False,
    )
    description = models.TextField(
        null=False,
        blank=False,
    )
    tools_description = models.TextField(null=False, blank=False)
