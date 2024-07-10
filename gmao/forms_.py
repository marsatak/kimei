from django import forms
from django.utils import timezone
from django.db.models import Max
from .models import Doleance, Station, Appelant, Client
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field


class DoleanceForm(forms.ModelForm):
    client = forms.ModelChoiceField(queryset=Client.objects.all(), empty_label="Sélectionnez un client")
    date_deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'class': 'flatpickr',
                'format': '%d-%m-%Y %H:%M',
            },
            input
        ),
        required=False,
        help_text="Date limite de l'intervention."
    )

    panne_declarer = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        help_text="Décrivez brièvement la panne."
    )

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

    element = forms.ChoiceField(required=False)

    class Meta:
        model = Doleance
        fields = [
            'client', 'station', 'appelant', 'type_transmission',
            'panne_declarer', 'element', 'type_contrat', 'date_deadline'
        ]

    def __init__(self, *args, **kwargs):
        super(DoleanceForm, self).__init__(*args, **kwargs)
        self.fields['station'].queryset = Station.objects.none()
        self.fields['appelant'].queryset = Appelant.objects.none()
        self.fields['element'].choices = [('', 'Sélectionnez un élément')]

        if not self.instance.pk:
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

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'client',
            'station',
            'appelant',
            'type_transmission',
            'panne_declarer',
            'element',
            'type_contrat',
            Field('date_deadline', css_class='flatpickr'),
        )

    def clean_date_deadline(self):
        date_deadline = self.cleaned_data.get('date_deadline')
        if not date_deadline:
            return timezone.now() + timezone.timedelta(days=1)
        return date_deadline

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.date_transmission = timezone.now()
        instance.statut = 'NEW'

        if commit:
            instance.save()
            self.generate_ndi(instance)

        return instance

    def generate_ndi(self, instance):
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
        instance.save()
