from django import forms
from django.utils import timezone
from django.db.models import Max
from .models import (
    Doleance, Station, Intervention,
    Appelant, Client,
    Personnel, Piste, AppareilDistribution, Cuve, Boutique, Servicing, Elec, Auvent, Totem
)


# class DoleanceForm(forms.ModelForm):
#     client = forms.ModelChoiceField(queryset=Client.objects.all(), empty_label="Sélectionnez un client")
#     TYPE_CONTRAT_CHOICES = [
#         ('', 'Sélectionnez un type de contrat'),
#         ('S', 'Sous Contrat'),
#         ('H', 'Hors Contrat'),
#         ('D', 'Devis'),
#         ('P', 'Préventive'),
#     ]
#
#     TRANSMISSION_CHOICES = [
#         ('', 'Sélectionnez un mode de transmission'),
#         ('Téléphone', 'Téléphone'),
#         ('Email', 'Email'),
#         ('Constatation', 'Constatation'),
#         ('Sms', 'Sms'),
#     ]
#
#     type_contrat = forms.ChoiceField(
#         choices=TYPE_CONTRAT_CHOICES,
#         required=True,
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )
#
#     type_transmission = forms.ChoiceField(
#         choices=TRANSMISSION_CHOICES,
#         required=True,
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )
#
#     class Meta:
#         model = Doleance
#         fields = ['client', 'station', 'appelant', 'type_transmission', 'panne_declarer', 'element', 'type_contrat']
#
#     def __init__(self, *args, **kwargs):
#         super(DoleanceForm, self).__init__(*args, **kwargs)
#         self.fields['station'].queryset = Station.objects.none()
#         self.fields['appelant'].queryset = Appelant.objects.none()
#
#         if 'client' in self.data:
#             try:
#                 client_id = int(self.data.get('client'))
#                 self.fields['station'].queryset = Station.objects.filter(client_id=client_id)
#                 self.fields['appelant'].queryset = Appelant.objects.filter(client_id=client_id)
#             except (ValueError, TypeError):
#                 pass
#         elif self.instance.pk and self.instance.station:
#             self.fields['client'].initial = self.instance.station.client
#             self.fields['station'].queryset = Station.objects.filter(client=self.instance.station.client)
#             self.fields['appelant'].queryset = Appelant.objects.filter(client=self.instance.station.client)
#
#     def save(self, commit=True):
#         instance = super().save(commit=False)
#
#         print("Entering save method")  # Debug print
#
#         instance.date_transmission = timezone.now()
#         instance.date_deadline = instance.date_transmission + timezone.timedelta(days=1)
#         instance.statut = 'NEW'
#
#         station = instance.station
#         client = station.client
#         year = timezone.now().strftime('%y')
#
#         last_ndi = Doleance.objects.filter(
#             station__client=client,
#             ndi__contains=f"/{client.nom_client}/{year}"
#         ).aggregate(Max('ndi'))['ndi__max']
#
#         if last_ndi:
#             last_num = int(last_ndi.split('/')[0])
#             new_num = last_num + 1
#         else:
#             new_num = 1
#
#         instance.ndi = f"{new_num:04d}/{client.nom_client}/{year}{instance.type_contrat}"
#
#         print(f"Generated NDI: {instance.ndi}")  # Debug print
#
#         if commit:
#             instance.save()
#
#         print("Exiting save method")  # Debug print
#         return instance


# forms.py


class DoleanceForm(forms.ModelForm):
    client = forms.ModelChoiceField(queryset=Client.objects.all(), empty_label="Sélectionnez un client")
    TYPE_CONTRAT_CHOICES = [
        ('', 'Sélectionnez un type de contrat'),
        ('S', 'Sous Contrat'),
        ('H', 'Hors Contrat'),
        ('D', 'Devis'),
        ('P', 'Préventive'),
    ]

    TRANSMISSION_CHOICES = [
        ('', 'Sélectionnez un mode de transmission'),
        ('Téléphone', 'Téléphone'),
        ('Email', 'Email'),
        ('Constatation', 'Constatation'),
        ('Sms', 'Sms'),
    ]

    type_contrat = forms.ChoiceField(
        choices=TYPE_CONTRAT_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    type_transmission = forms.ChoiceField(
        choices=TRANSMISSION_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    element = forms.CharField(required=False, widget=forms.Select())

    class Meta:
        model = Doleance
        fields = ['client', 'station', 'appelant', 'type_transmission', 'panne_declarer', 'element', 'type_contrat']

    def __init__(self, *args, **kwargs):
        super(DoleanceForm, self).__init__(*args, **kwargs)
        self.fields['station'].queryset = Station.objects.none()
        self.fields['appelant'].queryset = Appelant.objects.none()

        if 'client' in self.data:
            try:
                client_id = int(self.data.get('client'))
                self.fields['station'].queryset = Station.objects.filter(client_id=client_id)
                self.fields['appelant'].queryset = Appelant.objects.filter(client_id=client_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.station:
            self.fields['client'].initial = self.instance.station.client
            self.fields['station'].queryset = Station.objects.filter(client=self.instance.station.client)
            self.fields['appelant'].queryset = Appelant.objects.filter(client=self.instance.station.client)

        if 'station' in self.data:
            try:
                station_id = int(self.data.get('station'))
                self.fields['element'].choices = self.get_station_elements(station_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.station:
            self.fields['element'].choices = self.get_station_elements(self.instance.station.id)

    @staticmethod
    def get_station_elements(station_id):
        station = Station.objects.get(id=station_id)
        elements = [('', 'Sélectionnez un élément')]

        pistes = Piste.objects.filter(station=station)
        elements.extend([("piste_" + str(p.id), f"Piste {p.id}") for p in pistes])

        appareils = AppareilDistribution.objects.filter(piste__station=station)
        elements.extend([("appareil_" + str(a.id), f"Appareil {a.num_serie}") for a in appareils])

        cuves = Cuve.objects.filter(piste__station=station)
        elements.extend([("cuve_" + str(c.id), f"Cuve {c.libelle}") for c in cuves])

        if station.have_boutique:
            boutique = Boutique.objects.filter(station=station).first()
            if boutique:
                elements.append(("boutique_" + str(boutique.id), "Boutique"))

        if station.have_servicing:
            servicing = Servicing.objects.filter(station=station).first()
            if servicing:
                elements.append(("servicing_" + str(servicing.id), "Servicing"))

        elec = Elec.objects.filter(station=station)
        elements.extend([("elec_" + str(e.id), f"Électricité {e.id}") for e in elec])

        auvents = Auvent.objects.filter(piste__station=station)
        elements.extend([("auvent_" + str(a.id), f"Auvent {a.id}") for a in auvents])

        totems = Totem.objects.filter(piste__station=station)
        elements.extend([("totem_" + str(t.id), f"Totem {t.id}") for t in totems])

        return elements

    def save(self, commit=True):
        instance = super().save(commit=False)

        instance.date_transmission = timezone.now()
        instance.date_deadline = instance.date_transmission + timezone.timedelta(days=1)
        instance.statut = 'NEW'

        station = instance.station
        client = station.client
        year = timezone.now().strftime('%y')

        last_ndi = Doleance.objects.filter(
            station__client=client,
            ndi__contains=f"/{client.nom_client}/{year}"
        ).aggregate(Max('ndi'))['ndi__max']

        if last_ndi:
            last_num = int(last_ndi.split('/')[0])
            new_num = last_num + 1
        else:
            new_num = 1

        instance.ndi = f"{new_num:04d}/{client.nom_client}/{year}{instance.type_contrat}"

        if commit:
            instance.save()

        return instance


class InterventionForm(forms.ModelForm):
    personnels = forms.ModelMultipleChoiceField(
        queryset=Personnel.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Intervention
        fields = ['doleance', 'top_depart', 'top_debut', 'top_terminer', 'resolution']
        widgets = {
            'top_depart': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'top_debut': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'top_terminer': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doleance'].queryset = Doleance.objects.filter(statut='ENC')
