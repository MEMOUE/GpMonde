from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission, User
from django.core.mail import send_mail
from django.db import models
from django.conf import settings
from django.utils.crypto import get_random_string


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_active = False  # Désactiver l'utilisateur jusqu'à la vérification de l'email
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
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=False)  # Inactif jusqu'à vérification de l'email
    is_staff = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)  # Ajout pour suivre la vérification d'email
    verification_token = models.CharField(max_length=64, null=True, blank=True)  # Token de vérification

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def send_verification_email(self):
        # Générer un token unique pour la vérification
        verification_token = get_random_string(length=32)
        self.verification_token = verification_token
        self.save()

        verification_link = f"http://localhost:8080/verify-email/{verification_token}/"
        subject = 'Vérifiez votre adresse email'
        message = f'Bonjour {self.first_name},\n\nCliquez sur le lien pour vérifier votre adresse email : {verification_link}'
        send_mail(subject, message, 'no-reply@yourdomain.com', [self.email])

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
