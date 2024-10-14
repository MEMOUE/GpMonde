from datetime import timedelta

from django.http import JsonResponse
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.authtoken.admin import User
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import CompagnieTransport, TransporteurColis, AgenceVenteBillet, ProgrammeVoyage, AgenceEmballage, Offre
from .serializers import CompagnieTransportSerializer, TransporteurColisSerializer, AgenceVenteBilletSerializer, \
    ProgrammeVoyageSerializer, AgenceEmballageSerializer, BesoinSerializer, OffreSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Besoin, Notification


class CompagnieTransportViewSet(viewsets.ModelViewSet):
    queryset = CompagnieTransport.objects.all()
    serializer_class = CompagnieTransportSerializer
    #permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class TransporteurColisViewSet(viewsets.ModelViewSet):
    queryset = TransporteurColis.objects.all()
    serializer_class = TransporteurColisSerializer
    #permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user_id = self.request.data.get('user')
        if user_id:
            user = get_object_or_404(User, id=user_id)  # Importez User si nécessaire
            serializer.save(user=user)
        else:
            serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        user_id = self.request.data.get('user')
        if user_id:
            user = get_object_or_404(User, id=user_id)
            serializer.save(user=user)
        else:
            serializer.save(user=self.request.user)



class AgenceVenteBilletViewSet(viewsets.ModelViewSet):
    queryset = AgenceVenteBillet.objects.all()
    serializer_class = AgenceVenteBilletSerializer
    #permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        print(self.request.data)
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class ProgrammeVoyageViewSet(viewsets.ModelViewSet):
    queryset = ProgrammeVoyage.objects.all()
    serializer_class = ProgrammeVoyageSerializer
    #permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class AgenceEmballageViewSet(viewsets.ModelViewSet):
    queryset = AgenceEmballage.objects.all()
    serializer_class = AgenceEmballageSerializer
    #permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

class OffreViewSet(viewsets.ModelViewSet):
    queryset = Offre.objects.all()
    serializer_class = OffreSerializer
    #permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

def offres_actives(request):
    today = timezone.now()
    offres_actives = Offre.objects.filter(date_limite__gt=today)
    count = offres_actives.count()  # Compter les offres actives
    return JsonResponse({'count': count})

def besoins_actives(request):
    # Obtenir la date et l'heure actuelles
    now = timezone.now()
    # Calculer la date d'il y a 7 jours
    seven_days_ago = now - timedelta(days=7)

    # Filtrer les besoins créés dans les 7 derniers jours
    besoin_actives = Notification.objects.filter(created_at__gte=seven_days_ago)

    # Compter ces besoins actifs
    count = besoin_actives.count()

    # Retourner la réponse sous forme de JSON
    return JsonResponse({'count': count})


from rest_framework.decorators import api_view, permission_classes


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def submit_besoin(request):
    serializer = BesoinSerializer(data=request.data)
    if serializer.is_valid():
        # Sauvegarde le besoin dans la base de données
        besoin = serializer.save()

        # Créer une notification pour ce besoin
        notification_message = f' {besoin.message[:50]}'
        Notification.objects.create(besoin=besoin, message=notification_message)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_notifications(request):
    notifications = Notification.objects.all()  # Récupérer toutes les notifications
    notification_data = [
        {
            'id': notification.id,
            'message': notification.message,
            'created_at': notification.created_at,
            'is_read': notification.is_read
        }
        for notification in notifications
    ]
    return Response(notification_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def mark_notification_as_read(request):
    notification_id = request.data.get('id')
    try:
        notification = Notification.objects.get(id=notification_id)
        notification.is_read = True
        notification.save()
        return Response({'message': 'Notification marquée comme lue.'}, status=status.HTTP_200_OK)
    except Notification.DoesNotExist:
        return Response({'error': 'Notification non trouvée.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def mark_all_as_read(request):
    Notification.objects.filter(is_read=False).update(is_read=True)
    return Response({'message': 'Toutes les notifications marquées comme lues.'}, status=status.HTTP_200_OK)
