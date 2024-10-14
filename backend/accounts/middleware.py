import requests
from django.utils.timezone import now
from .models import VisitorActivityLog

class TrackUserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Obtenir l'IP du visiteur
        ip_address = self.get_ip(request)

        # Détecter l'utilisateur ou le visiteur
        user = request.user if request.user.is_authenticated else None

        # Enregistrer l'action et l'IP avec géolocalisation
        if ip_address:
            # Utiliser une API de géolocalisation pour récupérer la localisation à partir de l'IP
            location = self.get_geolocation(ip_address)
            action = f"visit_{request.path}"

            # Enregistrer l'activité
            VisitorActivityLog.objects.create(
                user=user,
                action=action,
                ip_address=ip_address,
                location=location
            )

        return response

    def get_ip(self, request):
        """ Récupérer l'adresse IP à partir des headers """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_geolocation(self, ip_address):
        """ Utiliser une API de géolocalisation pour obtenir la localisation depuis l'IP """
        try:
            # Utilisation d'un service de géolocalisation comme ipinfo.io ou freegeoip.app
            response = requests.get(f"https://ipinfo.io/{ip_address}/json")
            data = response.json()

            if 'city' in data and 'country' in data:
                return f"{data['city']}, {data['country']}"
            return "Unknown Location"
        except Exception as e:
            return "Unknown Location"
