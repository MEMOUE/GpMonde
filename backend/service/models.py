from django.db import models
from django.conf import settings  # Import to reference the AUTH_USER_MODEL

# Choix possibles pour le type de transport
TYPE_TRANSPORT_CHOICES = [
    ('terrestre', 'Terrestre'),
    ('maritime', 'Maritime'),
    ('aerien', 'Aérien'),
]

class CompagnieTransport(models.Model):
    nom = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=15)
    email = models.EmailField()
    pays = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    url = models.URLField(max_length=200, null=True, blank=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='compagnies',  # Optional: allows reverse lookup
        null=True,  # Optional: if you want to allow null values
        blank=True
    )

    def __str__(self):
        return self.nom


class TransporteurColis(models.Model):
    nom = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=15)
    email = models.EmailField()
    pays = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    type_transport = models.CharField(max_length=10, choices=TYPE_TRANSPORT_CHOICES, default='terrestre')
    url = models.URLField(max_length=200, null=True, blank=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transporteurs',  # Optional: allows reverse lookup
        null=True,
        blank=True
    )

    def __str__(self):
        return self.nom


class AgenceVenteBillet(models.Model):
    nom = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=15)
    email = models.EmailField()
    pays = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    url = models.URLField(max_length=200, null=True, blank=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='agences',  # Optional: allows reverse lookup
        null=True,
        blank=True
    )

    def __str__(self):
        return self.nom


class ProgrammeVoyage(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField()
    date_depart = models.DateTimeField()
    date_arrivee = models.DateTimeField()
    pays_depart = models.CharField(max_length=100)
    pays_arrivee = models.CharField(max_length=100, null=True, blank=True)  # Nouveau champ pour le pays d'arrivée
    telephone = models.CharField(max_length=20, null=True, blank=True)  # Nouveau champ pour le téléphone, non obligatoire
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='programmes',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.titre


class AgenceEmballage(models.Model):
    nom = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=15)
    email = models.EmailField()
    pays = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    url = models.URLField(max_length=200, null=True, blank=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='agences_emballage',  # Optional: allows reverse lookup
        null=True,  # Optional: if you want to allow null values
        blank=True
    )

    def __str__(self):
        return self.nom

class Offre(models.Model):
    nom = models.CharField(max_length=255)
    telephone = models.CharField(max_length=25)
    description = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    date_limite = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='offre',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.nom

class Besoin(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Besoin soumis : {self.message[:50]}'

class Notification(models.Model):
    besoin = models.ForeignKey(Besoin, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message