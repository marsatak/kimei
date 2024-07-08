import json
import logging
from datetime import datetime
from django.contrib import messages
from django.urls import reverse
from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt
from excel_response import ExcelResponse
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from django.db.models.functions import Substr, StrIndex
from django.db.models import Prefetch
from django.utils import timezone
from datetime import timedelta
from accounts.models import Employee, AbstractUser
from gmao.forms import DoleanceForm
from gmao.models import (
    Appelant, Client, Station, Doleance, Intervention,
    Poste, Personnel, Pointage,
    Boutique, Compresseur, Cuve, Piste, AppareilDistribution, Servicing, Elec, GroupeElectrogene,
    Auvent, Totem, Produit, Pistolet)
from gmao.serializers import (
    ClientSerializer, StationSerializer, DoleanceSerializer, InterventionSerializer,
    PosteSerializer, PersonnelSerializer, PointageSerializer,
    AppareilDistributionSerializer
)
from .models import Intervention, InterventionPersonnel
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.db.models import Min, Max
from django.core.exceptions import ValidationError
from django.db import DatabaseError
from django.db.models.functions import ExtractYear
from django.db.models.functions import TruncYear
from .models import Doleance, Intervention
from gmao_teams.models import EquipePersonnel, DoleanceEquipe
from django.http import JsonResponse
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from .models import Piece, UnitePiece, TypePiece
from gmao_teams.models import Equipe

logger = logging.getLogger(__name__)


# #####################Test######################
@require_http_methods(["GET", "POST"])
def test_view(request):
    print('post')
    return JsonResponse({'message': 'Test réussi'})


# #####################TimeStamp######################
def api_data(request):
    last_update = request.GET.get('last_update')

    if last_update:
        last_update = timezone.datetime.fromtimestamp(float(last_update))
        doleances = Doleance.objects.filter(modified_at__gt=last_update)
        interventions = Intervention.objects.filter(modified_at__gt=last_update)
        personnel = Personnel.objects.filter(modified_at__gt=last_update)
    else:
        doleances = Doleance.objects.all()
        interventions = Intervention.objects.all()
        personnel = Personnel.objects.all()

    has_new_data = doleances.exists() or interventions.exists() or personnel.exists()

    data = {
        'hasNewData': has_new_data,
        'timestamp': timezone.now().timestamp(),
        'data': {
            'doleances': list(doleances.values()),
            'interventions': list(interventions.values()),
            'personnel': list(personnel.values()),
        }
    }

    return JsonResponse(data)


def test_db_connection(request):
    try:
        count = Doleance.objects.using('kimei_db').count()
        return HttpResponse(f"Nombre de doléances : {count}")
    except Exception as e:
        return HttpResponse(f"Erreur : {str(e)}")


@login_required
def home(request):
    form = DoleanceForm()
    context = {
        'form': form,
        'user_role': request.user.role,
    }
    print(request.user.role)

    # if request.user.role == 'ADMIN':
    #     doleances = Doleance.objects.using('kimei_db').all()
    #     techniciens = Employee.objects.filter(role='TECH', statut='PRS')
    #     context.update({
    #         'doleances': doleances,
    #         'techniciens': techniciens,
    #     })
    #     equipes = Equipe.objects.using('teams_db').all()
    #     equipes_data = []
    #
    #     for equipe in equipes:
    #         doleance_ids = DoleanceEquipe.objects.using('teams_db').filter(equipe=equipe).values_list('doleance_id',
    #                                                                                                   flat=True)
    #         doleances = Doleance.objects.using('kimei_db').filter(id__in=doleance_ids).exclude(statut='TER')
    #
    #         equipes_data.append({
    #             'equipe': equipe,
    #             'doleances': doleances
    #         })
    #
    #     context['equipes_data'] = equipes_data
    if request.user.role == 'ADMIN':
        equipes = Equipe.objects.using('teams_db').all()
        equipes_data = []

        for equipe in equipes:
            # Récupérer les IDs des doléances pour cette équipe
            doleance_ids = list(DoleanceEquipe.objects.using('teams_db')
                                .filter(equipe=equipe)
                                .values_list('doleance_id', flat=True))

            # Récupérer les doléances correspondantes
            doleances = Doleance.objects.using('kimei_db').filter(id__in=doleance_ids).exclude(statut='TER')

            # Récupérer les IDs des techniciens pour cette équipe
            technicien_ids = list(EquipePersonnel.objects.using('teams_db')
                                  .filter(equipe=equipe)
                                  .values_list('personnel_id', flat=True))

            # Récupérer les techniciens correspondants
            techniciens = Personnel.objects.using('kimei_db').filter(id__in=technicien_ids)

            equipes_data.append({
                'id': equipe.id,
                'nom': equipe.nom,
                'description': equipe.description,
                'doleances': [
                    {
                        'id': d.id,
                        'ndi': d.ndi,
                        'panne_declarer': d.panne_declarer,
                        'statut': d.statut,
                        'date_transmission': d.date_transmission,
                        'station': d.station.libelle_station if d.station else None
                    } for d in doleances
                ],
                'techniciens': [
                    {
                        'id': t.id,
                        'nom': t.nom_personnel,
                        'prenom': t.prenom_personnel,
                        'statut': t.statut
                    } for t in techniciens
                ]
            })

        context['equipes_data'] = equipes_data
    elif request.user.role == 'TECH':
        personnel = Personnel.objects.using('kimei_db').get(matricule=request.user.matricule)
        equipe = EquipePersonnel.objects.using('teams_db').filter(personnel_id=personnel.id).first()
        if equipe:
            doleance_ids = DoleanceEquipe.objects.using('teams_db').filter(equipe=equipe.equipe).values_list(
                'doleance_id', flat=True)
            doleances = Doleance.objects.using('kimei_db').filter(id__in=doleance_ids)
            context.update({
                'doleances': doleances,
            })

    return render(request, 'gmao/home.html', context)


@api_view(['GET'])
def getDoleanceEncours(request):
    try:
        doleances = (
            (Doleance.objects.all())
            .exclude(statut='TER')
            .order_by('-date_deadline').filter(
                date_transmission__day=datetime.now().day,
                date_transmission__month=7,
                date_transmission__year=2024
            ))

        doleances_data = []
        for doleance in doleances:
            doleance_dict = DoleanceSerializer(doleance).data
            buttons = ''
            if doleance.statut == 'NEW':
                buttons += f'<button class="btn btn-primary btn-sm prendre-en-charge" data-id="{doleance.id}">Prendre en charge</button> '
            elif doleance.statut == 'ATT':
                intervention = Intervention.objects.filter(doleance=doleance, is_done=False).first()
                if intervention:
                    buttons += f'<button class="btn btn-success btn-sm commencer-intervention" data-id="{intervention.id}">Commencer</button> '
            elif doleance.statut == 'INT':
                intervention = Intervention.objects.filter(doleance=doleance, is_done=False).first()
                if intervention:
                    buttons += f'<button class="btn btn-warning btn-sm terminer-intervention" data-id="{intervention.id}">Terminer</button> '
            doleance_dict['actions'] = buttons
            doleances_data.append(doleance_dict)

        return Response(doleances_data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def getPoste(request):
    postes = Poste.objects.all()
    postes_serializer = PosteSerializer(postes, many=True)
    return Response(postes_serializer.data, content_type='application/json; charset=UTF-8')


# #####################Pointage Arrivée######################
@require_POST
def mark_arrivee(request, personnel_id):
    try:
        personnel = Personnel.objects.get(id=personnel_id)
        personnel.statut = 'PRS'
        personnel.save()
        return JsonResponse({'success': True, 'message': 'Arrivée marquée avec succès'})
    except Personnel.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Personnel non trouvé'}, status=404)


# #####################Pointage Départ######################

@require_POST
def mark_depart(request, personnel_id):
    try:
        personnel = Personnel.objects.get(id=personnel_id)
        personnel.statut = 'ABS'
        personnel.save()
        return JsonResponse({'success': True, 'message': 'Départ marqué avec succès'})
    except Personnel.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Personnel non trouvé'}, status=404)


# #####################Liste Personnel######################
@api_view(['GET'])
def getPersonnel(request):
    try:
        personnels = Personnel.objects.filter(is_active=True)
        personnels_serializer = PersonnelSerializer(personnels, many=True)
        return Response(personnels_serializer.data, content_type='application/json; charset=UTF-8')
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# #####################Maj Statut Personnel######################
@api_view(['PUT'])
def updatePersonnel(request, id):
    personnels = Personnel.objects.get(pk=id)
    personnels_serializer = PersonnelSerializer(personnels, data=request.data)
    if personnels_serializer.is_valid():
        personnels_serializer.save()
        return Response(personnels_serializer.data, content_type='application/json; charset=UTF-8')
    else:
        return Response(personnels_serializer.errors)


# #####################Liste Pointage######################
@api_view(['GET'])
def getPointage(request):
    pointages = (Pointage.objects.all()
                 .filter(date_heure_arrive__day=datetime.now().day)
                 .filter(date_heure_arrive__month=datetime.now().month)
                 .filter(date_heure_arrive__year=datetime.now().year))

    pointages_serializer = PointageSerializer(pointages, many=True)
    return Response(pointages_serializer.data)


# #####################Faire Un Pointage######################
@api_view(['POST'])
def postPointage(request):
    data = request.data
    personnel_id = data['personnel_id']
    today = timezone.now().date()

    existing_pointage = Pointage.objects.filter(
        personnel_id=personnel_id,
        date_heure_arrive__date=today
    ).first()

    if existing_pointage:
        return Response({'message': 'Un pointage existe déjà pour aujourd\'hui'}, status=status.HTTP_400_BAD_REQUEST)

    pointage = Pointage.objects.create(
        personnel_id=personnel_id,
        date_heure_arrive=timezone.now()
    )
    serializer = PointageSerializer(pointage)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
def putPointage(request, pk):
    serializer = PointageSerializer(data=request.data)
    try:
        personnel = (Personnel.objects
                     .filter(pointage__date_heure_arrive__day=datetime.now().day)
                     .get(id=pk))
    except Personnel.DoesNotExist:
        return Response({'error': 'Personnel non trouvé'}, status=status.HTTP_404_NOT_FOUND)
    print(pk)
    print(personnel)
    pointages = Pointage.objects.filter(personnel=personnel)
    pointage = pointages.get(date_heure_arrive__day=datetime.now().day)
    print(pointage)
    if pointage.date_heure_sortie is None:
        pointage.date_heure_sortie = datetime.now()
        diff = ((pointage.date_heure_sortie - pointage.date_heure_arrive)
                .total_seconds())
        pointage.seconde_actif = int(diff)
        serializer = PointageSerializer(pointage, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# #####################Réinitialiser Pointage######################
def resetPointage(request):
    personnels = Personnel.objects.all().filter(is_active=True)
    for personnel in personnels:
        personnel.statut = "ABS"
        personnel.save()
    return redirect('logout')


@csrf_exempt
@require_http_methods(["POST"])
def create_doleance(request):
    if request.method == 'POST':
        form = DoleanceForm(request.POST)
        if form.is_valid():
            doleance = form.save(commit=False)
            doleance.element = form.cleaned_data['element']
            doleance.panne_declarer = form.cleaned_data['panne_declarer'].upper()
            doleance.statut = "NEW"
            doleance.save()

            return JsonResponse({
                'success': True,
                'message': 'Doléance créée avec succès',
                'id': doleance.id
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    else:
        return JsonResponse({
            'success': False,
            'message': 'Méthode non autorisée'
        }, status=405)


def load_stations(request):
    client_id = request.GET.get('client')
    stations = Station.objects.filter(client_id=client_id).order_by('libelle_station')
    return JsonResponse(list(stations.values('id', 'libelle_station')), safe=False)


# #####################Récupérer la liste appelants ######################

def load_appelants(request):
    client_id = request.GET.get('client')
    logger.info(f"Tentative de chargement des appelants pour le client_id: {client_id}")
    try:
        appelants = Appelant.objects.filter(client_id=client_id).order_by('nom_appelant')
        logger.info(f"Nombre d'appelants trouvés: {appelants.count()}")
        data = list(appelants.values('id', 'nom_appelant', 'prenom_appelant'))
        return JsonResponse(data, safe=False)
    except DatabaseError as e:
        logger.error(f"Erreur de base de données lors du chargement des appelants: {str(e)}")
        return JsonResponse({'error': 'Erreur de base de données'}, status=500)
    except Exception as e:
        logger.error(f"Erreur inattendue lors du chargement des appelants: {str(e)}")
        return JsonResponse({'error': 'Erreur serveur inattendue'}, status=500)


def load_elements(request):
    station_id = request.GET.get('station')
    if not station_id:
        return JsonResponse([], safe=False)

    station = Station.objects.get(id=station_id)
    appareils = AppareilDistribution.objects.filter(piste__station=station)
    pistolets = Pistolet.objects.filter(appareil_distribution__piste__station=station).order_by('appareil_distribution',
                                                                                                'orientation')

    elements = {
        'Appareil de distribution': [],
        'Pistolets': [],
        'Autres': [('lot_station', f'LOT STATION {station.libelle_station}')]
    }

    for appareil in appareils:
        if appareil.face_principal and appareil.face_secondaire and appareil.num_serie and appareil.type_contrat:
            element = f"{appareil.face_principal}/{appareil.face_secondaire}-{appareil.num_serie}-{appareil.type_contrat}"
            elements['Appareil de distribution'].append((f"appareil_{appareil.id}", element))

    for pistolet in pistolets:
        appareil = pistolet.appareil_distribution
        orientation = pistolet.orientation[0] if pistolet.orientation else ''
        if orientation in ['R', 'L']:
            number = int(appareil.face_principal) if orientation == 'R' else int(appareil.face_secondaire)
            if appareil.num_serie and pistolet.produit and pistolet.produit.code_produit and pistolet.type_contrat:
                element = f"{number}-{appareil.num_serie}{orientation}-{pistolet.produit.code_produit}-{pistolet.type_contrat}"
                elements['Pistolets'].append((f"pistolet_{pistolet.id}", element))

    return JsonResponse(elements)


@require_http_methods(["GET", "POST"])
def commencer_intervention(request, intervention_id):
    try:
        intervention = get_object_or_404(Intervention, id=intervention_id)
        kilometrage = request.POST.get('kilometrage')
        if intervention.etat_doleance != 'ATT':
            return JsonResponse({'success': False, 'message': 'L\'intervention n\'est pas en attente'})

        if not intervention.top_debut:
            intervention.top_debut = timezone.now()
            intervention.is_half_done = True
            intervention.etat_doleance = 'INT'
            intervention.kilometrage_depart_debut = kilometrage
            intervention.save()

        doleance = intervention.doleance
        doleance.statut = 'INT'
        doleance.save()

        intervention_personnels = InterventionPersonnel.objects.filter(intervention=intervention)
        for intervention_personnel in intervention_personnels:
            technicien = intervention_personnel.personnel
            technicien.statut = 'INT'
            technicien.save()

        return JsonResponse({
            'success': True,
            'message': 'Intervention déclenchée avec succès',
            'intervention_id': intervention.id,
            'top_debut': intervention.top_debut.strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@require_GET
def get_techniciens_disponibles(request):
    techniciens = Personnel.objects.filter(statut='PRS')
    return JsonResponse({
        'success': True,
        'techniciens': list(techniciens.values('id', 'nom_personnel', 'prenom_personnel'))
    })


# #####################Déclencher une intervention######################

@require_POST
def declencher_intervention(request, doleance_id):
    doleance = get_object_or_404(Doleance, id=doleance_id)

    if doleance.statut not in ['NEW', 'ATP', 'ATD']:
        return JsonResponse({'success': False, 'message': 'Cette doléance ne peut pas être traitée'})

    data = json.loads(request.body)
    techniciens_ids = data.get('techniciens', [])

    intervention = Intervention.objects.create(
        doleance=doleance,
        top_depart=timezone.now(),
        is_done=False,
        is_half_done=False,
        is_going_home=False,
        etat_doleance='ATT'
    )

    doleance.statut = 'ATT'
    doleance.date_debut = timezone.now()
    doleance.save()

    for tech_id in techniciens_ids:
        technicien = Personnel.objects.get(id=tech_id)
        InterventionPersonnel.objects.create(intervention=intervention, personnel=technicien)
        technicien.statut = 'ATT'  # Le technicien est en attente
        technicien.save()

    return JsonResponse({
        'success': True,
        'message': 'Intervention déclenchée avec succès',
        'intervention_id': intervention.id
    })


# #####################Annuler une intervention######################
@require_POST
def annuler_intervention(request, intervention_id):
    try:
        intervention = get_object_or_404(Intervention, id=intervention_id)
        doleance = intervention.doleance
        ancien_statut = doleance.statut
        intervention_personnels = InterventionPersonnel.objects.filter(intervention=intervention)
        for intervention_personnel in intervention_personnels:
            technicien = intervention_personnel.personnel
            technicien.statut = 'PRS'
            technicien.save()
        if ancien_statut in ['ATP', 'ATD']:
            doleance.statut = ancien_statut
        else:
            doleance.statut = 'NEW'
        doleance.save()
        # Réinitialiser l'intervention
        intervention.delete()

        return JsonResponse({
            'success': True,
            'message': 'Intervention annulée avec succès',
            'nouveau_statut': doleance.statut
        })
    except Intervention.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Intervention non trouvée'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
def liste_interventions(request):
    current_date = timezone.now().date()

    if request.user.role == 'ADMIN':
        interventions = Intervention.objects.filter(
            top_depart__date=current_date
        ).order_by('-top_depart')
    elif request.user.role == 'TECH':
        try:
            personnel = Personnel.objects.get(matricule=request.user.matricule)
            interventions = Intervention.objects.filter(
                id__in=InterventionPersonnel.objects.filter(personnel=personnel).values('intervention_id'),
                top_depart__date=current_date
            ).order_by('-top_depart')
        except Personnel.DoesNotExist:
            interventions = Intervention.objects.none()
    else:
        interventions = Intervention.objects.none()

    # Récupérer les techniciens pour chaque intervention
    intervention_ids = [i.id for i in interventions]
    intervention_personnel = InterventionPersonnel.objects.filter(
        intervention_id__in=intervention_ids
    ).select_related('personnel')

    # Créer un dictionnaire pour stocker les techniciens par intervention
    techniciens_par_intervention = {i.id: [] for i in interventions}
    for ip in intervention_personnel:
        techniciens_par_intervention[ip.intervention_id].append(ip.personnel)

    # Ajouter les techniciens à chaque intervention
    for intervention in interventions:
        intervention.techniciens = techniciens_par_intervention[intervention.id]

    context = {
        'interventions': interventions,
        'current_date': current_date,
    }

    return render(request, 'gmao/liste_interventions.html', context)


def detail_intervention(request, intervention_id):
    intervention = get_object_or_404(Intervention, id=intervention_id)
    techniciens = (InterventionPersonnel.objects.filter(intervention=intervention)
                   .all().select_related('personnel'))
    print("Techniciens associés:", [t.personnel.nom_personnel for t in techniciens])  # Ajoutez cette ligne
    return render(request, 'gmao/detail_intervention.html', {
        'intervention': intervention,
        'techniciens': techniciens
    })


@csrf_exempt
@require_POST
def terminer_travail(request, intervention_id):
    try:
        intervention = get_object_or_404(Intervention, id=intervention_id)

        statut_final = request.POST.get('statut_final', '').upper()

        if not statut_final or statut_final not in ['TER', 'ATP', 'ATD']:
            return JsonResponse({'success': False, 'message': f'Statut final invalide: {statut_final}'})

        # Traitement du numéro de fiche
        numero_fiche = request.POST.get('numero_fiche', '')
        try:
            numero_fiche = int(numero_fiche)
            if numero_fiche < 0 or numero_fiche > 99999:
                return JsonResponse({'success': False, 'message': 'Le numéro de fiche doit être entre 0 et 99999'})

            numero_fiche_complet = f"00{numero_fiche:05d}"

            if Intervention.objects.filter(numero_fiche=numero_fiche_complet).exists():
                return JsonResponse({'success': False, 'message': 'Ce numéro de fiche est déjà utilisé'})

            intervention.numero_fiche = numero_fiche_complet
        except ValueError:
            return JsonResponse({'success': False, 'message': 'Le numéro de fiche doit être un nombre entier'})

        # Le reste du code pour mettre à jour l'intervention
        intervention.is_done = True
        intervention.etat_doleance = statut_final
        intervention.description_panne = request.POST.get('description_panne', '').upper()
        intervention.resolution = request.POST.get('resolution', '').upper()
        intervention.observations = request.POST.get('observations', '').upper()
        intervention.pieces_changees = request.POST.get('pieces_changees', '').upper()
        intervention.top_terminer = timezone.now()

        # Calculer la durée de l'intervention
        if intervention.top_debut:
            duree = intervention.top_terminer - intervention.top_debut
            intervention.duree_intervention = int(duree.total_seconds())
        else:
            intervention.duree_intervention = 0

        intervention.save()

        # Mise à jour de la doléance
        doleance = intervention.doleance
        doleance.statut = statut_final
        interventions = Intervention.objects.filter(doleance=doleance)
        doleance.date_debut = interventions.aggregate(Min('top_debut'))['top_debut__min']
        doleance.date_fin = interventions.aggregate(Max('top_terminer'))['top_terminer__max']
        doleance.save()

        # Mise à jour des techniciens
        for intervention_personnel in InterventionPersonnel.objects.filter(intervention=intervention):
            personnel = intervention_personnel.personnel
            personnel.statut = 'PRS'
            personnel.save()

        return JsonResponse({
            'success': True,
            'message': 'Intervention terminée avec succès',
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Erreur inattendue: {str(e)}'})


@login_required
@require_GET
def get_available_years(request):
    try:
        years = (
            Doleance.objects.using('kimei_db')
            .annotate(year=ExtractYear('date_transmission'))
            .values_list('year', flat=True)
            .distinct()
            .order_by('-year')
        )
        return JsonResponse({'years': list(years)})
    except Exception as e:
        logger.error(f"Erreur dans get_available_years: {str(e)}", exc_info=True)
        return JsonResponse({'error': 'Erreur serveur inattendue'}, status=500)


@login_required
def toutes_les_doleances(request):
    years = Doleance.objects.annotate(year=ExtractYear('date_transmission')) \
        .values_list('year', flat=True) \
        .distinct() \
        .order_by('-year')
    months = [
        (1, 'Janvier'), (2, 'Février'), (3, 'Mars'), (4, 'Avril'),
        (5, 'Mai'), (6, 'Juin'), (7, 'Juillet'), (8, 'Août'),
        (9, 'Septembre'), (10, 'Octobre'), (11, 'Novembre'), (12, 'Décembre')
    ]
    current_year = datetime.now().year
    current_month = datetime.now().month
    return render(request, 'gmao/toutes_les_doleances.html', {
        'years': years,
        'months': months,
        'current_year': current_year,
        'current_month': current_month
    })


@login_required
def get_doleances_data(request):
    year = request.GET.get('year')
    month = request.GET.get('month')
    start_date = request.GET.get('startDate')
    end_date = request.GET.get('endDate')

    doleances_query = Doleance.objects.all()

    if year and year != 'all':
        doleances_query = doleances_query.filter(date_transmission__year=year)

    if month and month != 'all':
        doleances_query = doleances_query.filter(date_transmission__month=month)

    if start_date and end_date:
        doleances_query = doleances_query.filter(
            date_transmission__range=[start_date, end_date]
        )

    doleances = doleances_query.exclude(statut='NEW').order_by('-date_transmission')

    data = [{
        'id': d.id,
        'ndi': d.ndi,
        'date_transmission': d.date_transmission.strftime('%d/%m/%Y %H:%M'),
        'statut': d.statut,
        'station': d.station.libelle_station,
        'element': d.element,
        'panne_declarer': d.panne_declarer,
        'date_deadline': d.date_deadline.strftime('%d/%m/%Y %H:%M') if d.date_deadline else '',
        'commentaire': d.commentaire,
    } for d in doleances]

    return JsonResponse({'data': data})


@login_required
@require_POST
def prendre_en_charge(request, doleance_id):
    logger.info(f"Tentative de prise en charge de la doléance {doleance_id}")
    try:
        doleance = get_object_or_404(Doleance.objects.using('kimei_db'), id=doleance_id)
        logger.info(f"Doléance trouvée: {doleance} {doleance.statut}")

        if doleance.statut not in ['NEW', 'ATP', 'ATD']:
            return JsonResponse({'success': False, 'message': 'Cette doléance ne peut pas être prise en charge'})

        technicien = Personnel.objects.using('kimei_db').get(matricule=request.user.matricule)
        logger.info(f"Technicien trouvé: {technicien}")

        equipe_personnel = EquipePersonnel.objects.using('teams_db').filter(personnel_id=technicien.id).first()
        logger.info(f"EquipePersonnel trouvé: {equipe_personnel}")

        if not equipe_personnel:
            return JsonResponse({'success': False, 'message': 'Ce technicien n\'appartient à aucune équipe'})

        equipe = equipe_personnel.equipe
        logger.info(f"Équipe trouvée: {equipe}")

        # Vérifier si la doléance est déjà associée à une équipe
        # existing_association = DoleanceEquipe.objects.using('teams_db').filter(doleance_id=doleance.id).first()
        # if existing_association:
        #     if existing_association.equipe_id != equipe.id:
        #         # Si la doléance est associée à une autre équipe, la dissocier
        #         existing_association.delete()
        #     else:
        #         # Si la doléance est déjà associée à cette équipe, ne rien faire
        #         logger.info(f"La doléance {doleance_id} est déjà associée à l'équipe {equipe.id}")
        #         return JsonResponse({
        #             'success': True,
        #             'message': 'Cette doléance est déjà prise en charge par votre équipe',
        #             'intervention_id': None
        #         })

        intervention = Intervention.objects.using('kimei_db').create(
            doleance=doleance,
            top_depart=timezone.now(),
            is_done=False,
            is_half_done=False,
            is_going_home=False,
            etat_doleance='ATT'
        )
        logger.info(f"Intervention créée: {intervention}")

        doleance.statut = 'ATT'
        doleance.save(using='kimei_db')

        membres_equipe = Personnel.objects.using('kimei_db').filter(id__in=equipe.get_personnel_ids())
        for membre in membres_equipe:
            InterventionPersonnel.objects.using('kimei_db').create(intervention=intervention, personnel=membre)
            membre.statut = 'ATT'
            membre.save(using='kimei_db')

        # Créer ou mettre à jour l'association DoleanceEquipe
        DoleanceEquipe.objects.using('teams_db').update_or_create(
            equipe=equipe,
            doleance_id=doleance.id,
            defaults={'equipe': equipe, 'doleance_id': doleance.id}
        )

        return JsonResponse({
            'success': True,
            'message': 'Doléance prise en charge avec succès par l\'équipe',
            'intervention_id': intervention.id,
            'redirect_url': reverse('gmao:detail_intervention', args=[intervention.id])
        })
    except Exception as e:
        logger.error(f"Erreur lors de la prise en charge: {str(e)}", exc_info=True)
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
@require_POST
def annuler_prise_en_charge(request, intervention_id):
    try:

        intervention = get_object_or_404(Intervention, id=intervention_id)
        doleance = intervention.doleance
        doleance.statut = 'NEW'
        doleance.save()

        # Réinitialiser l'intervention
        intervention.delete()

        # Réinitialiser la doléance

        # Réinitialiser le statut des techniciens
        intervention_personnels = InterventionPersonnel.objects.filter(intervention=intervention)
        for intervention_personnel in intervention_personnels:
            technicien = intervention_personnel.personnel
            technicien.statut = 'PRS'
            technicien.save()

        # Supprimer l'association de la doléance à l'équipe
        DoleanceEquipe.objects.filter(doleance=doleance).delete()

        return JsonResponse({
            'success': True,
            'message': 'Prise en charge annulée avec succès',
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@require_POST
@login_required
def affecter_techniciens(request, doleance_id):
    if request.user.role != 'ADMIN':
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=403)

    data = json.loads(request.body)
    technicien_ids = data.get('techniciens', [])

    try:
        doleance = Doleance.objects.using('kimei_db').get(id=doleance_id)
        techniciens = Personnel.objects.using('kimei_db').filter(id__in=technicien_ids)

        intervention = Intervention.objects.using('kimei_db').create(
            doleance=doleance,
            top_depart=timezone.now(),
            is_done=False,
            is_half_done=False,
            etat_doleance='ATT'
        )

        for technicien in techniciens:
            InterventionPersonnel.objects.using('kimei_db').create(intervention=intervention, personnel=technicien)
            technicien.statut = 'ATT'
            technicien.save()

        doleance.statut = 'ATT'
        doleance.save()

        return JsonResponse({'success': True, 'message': 'Techniciens affectés avec succès'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
def get_technicien_portfolio(request):
    if request.user.role != 'TECH':
        return JsonResponse({'success': False, 'message': 'Accès non autorisé'})

    personnel = Personnel.objects.using('kimei_db').get(matricule=request.user.matricule)
    equipe = EquipePersonnel.objects.using('teams_db').filter(personnel_id=personnel.id).first()

    if not equipe:
        return JsonResponse({
            'success': True,
            'doleances': [],
            'message': 'Aucune équipe assignée'
        })

    doleance_ids = list(DoleanceEquipe.objects.using('teams_db')
                        .filter(equipe=equipe.equipe)
                        .values_list('doleance_id', flat=True))

    # Exclure les doléances terminées
    doleances = Doleance.objects.using('kimei_db').filter(id__in=doleance_ids).exclude(statut='TER')

    # Vérifier si une intervention est en cours pour cette équipe
    intervention_en_cours = Intervention.objects.using('kimei_db').filter(
        doleance__in=doleances,
        is_half_done=True,
        is_done=False
    ).exists()

    doleances_data = []
    # for d in doleances:
    #     intervention = Intervention.objects.using('kimei_db').filter(doleance=d).first()
    #     doleances_data.append({
    #         'id': d.id,
    #         'ndi': d.ndi,
    #         'station': d.station.libelle_station,
    #         'element': d.element,
    #         'panne_declarer': d.panne_declarer,
    #         'statut': d.statut,
    #         'intervention_id': intervention.id if intervention else None
    #     })
    for d in doleances:
        intervention = Intervention.objects.using('kimei_db').filter(doleance=d).first()
        doleances_data.append({
            'id': d.id,
            'ndi': d.ndi,
            'station': d.station.libelle_station,
            'element': d.element,
            'panne_declarer': d.panne_declarer,
            'statut': d.statut,
            'intervention_id': intervention.id if intervention else None,
            'intervention_en_cours': intervention.is_half_done if intervention else False
        })

    return JsonResponse({
        'success': True,
        'doleances': doleances_data,
        'equipe': equipe.equipe.nom if equipe else None,
        'intervention_en_cours': True
    })


@login_required
def toutes_les_pieces(request):
    return render(request, 'gmao/toutes_les_pieces.html')


def get_pieces_data(request):
    pieces = Piece.objects.all()

    # Sérialiser les objets Piece en JSON
    pieces_json = serialize('json', pieces)
    pieces_data = json.loads(pieces_json)

    # Transformer les données sérialisées en un format plus simple
    formatted_data = []
    for item in pieces_data:
        piece = item['fields']
        piece['id'] = item['pk']  # Ajouter l'ID à chaque objet

        # Gérer les relations ForeignKey
        if piece['unite']:
            unite = UnitePiece.objects.get(pk=piece['unite'])
            piece['unite'] = unite.unite if hasattr(unite, 'unite') else str(unite)

        if piece['type']:
            type_piece = TypePiece.objects.get(pk=piece['type'])
            piece['type'] = type_piece.libelle_type if hasattr(type_piece, 'libelle_type') else str(type_piece)

        formatted_data.append(piece)

    # Retourner les données au format JSON
    return JsonResponse({'data': formatted_data}, safe=False)
