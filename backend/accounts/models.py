from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission, User
from django.db import models
from django.conf import settings



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Add related_name to avoid reverse accessor conflicts
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Unique related name for groups
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Unique related name for user_permissions
        blank=True
    )

    def __str__(self):
        return self.email



class VisitorActivityLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)  # Utilise AUTH_USER_MODEL ici
    action = models.CharField(max_length=255)  # L'action effectuée
    timestamp = models.DateTimeField(auto_now_add=True)  # Date et heure de l'action
    ip_address = models.GenericIPAddressField()  # Adresse IP du visiteur ou utilisateur
    location = models.CharField(max_length=255, null=True, blank=True)  # Localisation géographique

    def __str__(self):
        if self.user:
            return f"{self.user} - {self.action} at {self.timestamp}"
        else:
            return f"Visitor - {self.action} at {self.timestamp}"
