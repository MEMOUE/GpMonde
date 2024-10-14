from rest_framework import serializers
from .models import CompagnieTransport, TransporteurColis, AgenceVenteBillet, ProgrammeVoyage, \
    AgenceEmballage, Besoin, Offre


class CompagnieTransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompagnieTransport
        fields = '__all__'
        read_only_fields = ('user',)

class TransporteurColisSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransporteurColis
        fields = '__all__'
        read_only_fields = ('user',)

class AgenceVenteBilletSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgenceVenteBillet
        fields = '__all__'
        read_only_fields = ('user',)

class ProgrammeVoyageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgrammeVoyage
        fields = '__all__'
        read_only_fields = ('user',)

class AgenceEmballageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgenceEmballage
        fields = '__all__'
        read_only_fields = ('user',)

class OffreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offre
        fields = '__all__'
        read_only_fields = ('user',)



class BesoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Besoin
        fields = ['id', 'message', 'created_at']