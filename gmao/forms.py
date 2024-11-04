from django import forms
from django.utils import timezone
from django.db.models import Max
from .models import (
    Doleance, Station, Intervention,
    Appelant, Client,
    Personnel, Piste, AppareilDistribution, Cuve, Boutique, Servicing, Elec, Auvent, Totem
)
from gmao.models import (
    Poste, Personnel, Pointage,
    Boutique, Compresseur, Cuve, Piste, AppareilDistribution, Servicing, Elec, GroupeElectrogene,
    Auvent, Totem, Produit, Pistolet, Tgbt, EclairageElectricite)
from django.db.models import Q


# PARAMETRAGE FORMULAIRE DE SAISIE ET DE MAJ DES DOLEANCES
class DoleanceForm(forms.ModelForm):
    client = forms.ModelChoiceField(queryset=Client.objects.all(), empty_label="Sélectionnez un client")
    date_deadline = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(
            attrs={
                'class': 'flatpickr',
                # 'type': 'datetime-local',
            },

            format='%d/%m/%Y %H:%M'),
        input_formats=['%d/%m/%Y %H:%M']
    )

    panne_declarer = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}),  # Réduisez le nombre de lignes à 3
        help_text="Décrivez brièvement la panne ."
    )
    commentaire = forms.CharField(required=False,
                                  widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}),
                                  # Réduisez le nombre de lignes à 3
                                  help_text="Rajouter un commentaire ."
                                  )
    TYPE_CONTRAT_CHOICES = [
        ('', 'Sélectionnez un type de contrat'),
        ('S', 'Sous Contrat'),
        ('H', 'Hors Contrat'),
        ('D', 'Devis'),
        ('C', 'Conso'),
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

    # element = forms.ChoiceField(
    #     choices=[],
    #     required=False,
    # )

    class Meta:
        model = Doleance
        fields = [
            'client', 'station', 'appelant', 'date_transmission', 'type_transmission',
            'panne_declarer', 'element', 'type_contrat', 'date_deadline', 'commentaire']

    def clean(self):
        cleaned_data = super().clean()
        # Ajoutez ici toute logique de validation supplémentaire si nécessaire
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(DoleanceForm, self).__init__(*args, **kwargs)
        self.fields['station'].queryset = Station.objects.none()
        self.fields['appelant'].queryset = Appelant.objects.none()
        self.fields['element'].choices = [('', 'Sélectionnez un élément')]
        if not self.instance.pk:
            # Si c'est une nouvelle instance, définir la valeur par défaut
            self.fields['date_transmission'].widget.attrs['class'] = 'flatpickr'
            self.fields['date_deadline'].widget.attrs['class'] = 'flatpickr'

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
        elements = {
            'Appareil de distribution': [],
            'Pistolets': [],
            'Cuves': [],
            'Servicing': [],
            'Électricité': [],
            'Autres': [('lot_station', f'Lot-Station-{station.libelle_station}')]
        }

        appareils = AppareilDistribution.objects.filter(piste__station=station)
        for appareil in appareils:
            if appareil.face_principal and appareil.face_secondaire and appareil.num_serie and appareil.type_contrat:
                element = f"{appareil.face_principal}/{appareil.face_secondaire}-{appareil.num_serie}-{appareil.type_contrat}"
                elements['Appareil de distribution'].append((f"appareil_{appareil.id}", element))

        pistolets = Pistolet.objects.filter(appareil_distribution__piste__station=station).order_by(
            'appareil_distribution', 'orientation')
        for pistolet in pistolets:
            appareil = pistolet.appareil_distribution
            orientation = pistolet.orientation[0] if pistolet.orientation else ''
            if orientation in ['R', 'L']:
                number = int(appareil.face_principal) if orientation == 'R' else int(appareil.face_secondaire)
                if appareil.num_serie and pistolet.produit and pistolet.produit.code_produit and pistolet.type_contrat:
                    element = f"{number}-{appareil.num_serie}{orientation}-{pistolet.produit.code_produit}-{pistolet.type_contrat}"
                    elements['Pistolets'].append((f"pistolet_{pistolet.id}", element))

        cuves = Cuve.objects.filter(piste__station=station)
        for cuve in cuves:
            element_info = f"Cuve {cuve.libelle} - {cuve.produit.nom_produit} - {cuve.capacite}L - {cuve.type_contrat}"
            elements['Cuves'].append((f"cuve_{cuve.id}", element_info))

        if station.have_servicing:
            servicing = Servicing.objects.filter(station=station).first()
            if servicing:
                element = f"Servicing-{station.libelle_station}"
                elements['Servicing'].append((f"servicing_{servicing.id}", element))

        elec = Elec.objects.filter(station=station).first()
        if elec:
            elements['Électricité'].append(("elec_" + str(elec.id), "Électricité générale"))

            groupes = GroupeElectrogene.objects.filter(electricite=elec)
            for groupe in groupes:
                element_info = f"GE - {groupe.type.libelle_type} - {groupe.type_contrat}"
                elements['Électricité'].append((f"groupe_electrogene_{groupe.id}", element_info))

            tgbts = Tgbt.objects.filter(electricite=elec)
            for tgbt in tgbts:
                element_info = f"TGBT - {tgbt.type.libelle_type} - {tgbt.modele.libelle_modele} - {tgbt.type_contrat}"
                elements['Électricité'].append((f"tgbt_{tgbt.id}", element_info))

            eclairages = EclairageElectricite.objects.filter(electricite=elec)
            for eclairage in eclairages:
                element_info = f"Éclairage - {eclairage.type.libelle_type} - {eclairage.modele.libelle_modele} - {eclairage.type_contrat}"
                elements['Électricité'].append((f"eclairage_elec_{eclairage.id}", element_info))

        auvents = Auvent.objects.filter(piste__station=station)
        elements['Autres'].extend([("auvent_" + str(a.id), f"Auvent {a.id}") for a in auvents])

        totems = Totem.objects.filter(piste__station=station)
        elements['Autres'].extend([("totem_" + str(t.id), f"Totem {t.id}") for t in totems])

        return elements

    def clean_date_deadline(self):
        date = self.cleaned_data.get('date_deadline')
        if date:
            if timezone.is_naive(date):
                return timezone.make_aware(date)
            return date
        return None

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.pk:
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
        else:
            existing_instance = Doleance.objects.get(pk=instance.pk)
            instance.ndi = existing_instance.ndi
            instance.date_transmission = existing_instance.date_transmission
            instance.statut = existing_instance.statut

        if commit:
            instance.save()

        return instance


# FIN PARAMETRAGE FORMULAIRE DE SAISIE ET DE MAJ DES DOLEANCES

# PARAMETRAGE FORMULAIRE DE SAISIE ET DE MAJ DES INTERVENTIONS
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
# FIN PARAMETRAGE FORMULAIRE DE SAISIE ET DE MAJ DES INTERVENTIONS
