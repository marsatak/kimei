from rest_framework import serializers
from .models import (Poste, Personnel, Pointage,
                     Appelant, Station, Client,
                     Doleance, Intervention,
                     Piste, AppareilDistribution, ModeleAd,
                     )


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class AppelantSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)

    class Meta:
        model = Appelant
        fields = '__all__'


class PisteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Piste
        fields = '__all__'


class ModeleAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModeleAd
        fields = '__all__'


class StationSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)

    class Meta:
        model = Station
        fields = ['client', 'libelle_station']


class DoleanceSerializer(serializers.ModelSerializer):
    station = StationSerializer(read_only=True)
    date_transmission = serializers.DateTimeField(required=False,
                                                  format='%Y-%m-%d %H:%M:%S')  # format='%d/%m/%Y %H:%M')
    date_deadline = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    date_debut = serializers.DateTimeField(allow_null=True, required=False, format='%Y-%m-%d %H:%M:%S')
    date_fin = serializers.DateTimeField(allow_null=True, required=False, format='%Y-%m-%d %H:%M:%S')
    appelant = AppelantSerializer(read_only=True)

    class Meta:
        model = Doleance
        fields = '__all__'


class PosteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poste
        fields = '__all__'


class PersonnelSerializer(serializers.ModelSerializer):
    poste = PosteSerializer(read_only=True)
    last_visite_medical = serializers.DateTimeField(required=False, format='%d/%m/%Y %H:%M')

    class Meta:
        model = Personnel
        fields = '__all__'


class PointageSerializer(serializers.ModelSerializer):
    personnel = PersonnelSerializer(read_only=True)

    class Meta:
        model = Pointage
        fields = '__all__'


class InterventionSerializer(serializers.ModelSerializer):
    doleance = DoleanceSerializer(read_only=True)
    top_depart = serializers.DateTimeField(required=False, format='%d/%m/%Y %H:%M')
    top_debut = serializers.DateTimeField(required=False, format='%d/%m/%Y %H:%M')
    top_terminer = serializers.DateTimeField(required=False, format='%d/%m/%Y %H:%M')

    class Meta:
        model = Intervention
        fields = '__all__'


class AppareilDistributionSerializer(serializers.ModelSerializer):
    piste = PisteSerializer(read_only=True)
    station = StationSerializer(read_only=True)
    modele_ad = ModeleAdSerializer(read_only=True)

    class Meta:
        model = AppareilDistribution
        fields = '__all__'
