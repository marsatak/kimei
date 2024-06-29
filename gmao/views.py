import json
import logging
from datetime import datetime
from django.contrib import messages
from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404

from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt
from excel_response import ExcelResponse
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from django.db.models.functions import Substr, StrIndex

from django.utils import timezone

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

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import logging

logger = logging.getLogger(__name__)


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


# #####################Home Page######################
@login_required(login_url='login')
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    return render(request, 'gmao/home.html', )


# #####################Liste Doléances En Cours######################


@api_view(['GET'])
def getDoleanceEncours(request):
    try:
        # current_date = timezone.now()
        doleances = (Doleance.objects.all()
                     .filter(date_transmission__day=datetime.now().day)
                     .exclude(statut='TER')
                     .filter(date_transmission__year=datetime.now().year,
                             date_transmission__month=datetime.now().month)
                     .order_by('-date_transmission'))

        doleances_serializer = DoleanceSerializer(doleances, many=True)
        return Response(doleances_serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# #####################Liste Poste######################
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
    date_heure_arrive = datetime.now()
    data = request.data
    pointageToday = (Pointage.objects.all()
                     .filter(date_heure_arrive__month=datetime.now().month)
                     .filter(date_heure_arrive__year=datetime.now().year)
                     .filter(date_heure_arrive__day=datetime.now().day)
                     .filter(personnel_id=data['personnel_id']))
    if pointageToday:
        print(pointageToday)
    else:
        pointage = Pointage.objects.create(
            personnel_id=data['personnel_id'],
            date_heure_arrive=date_heure_arrive)
        serializer = PointageSerializer(pointage, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# #####################Maj Statut Pointage Pour Un Personnel######################
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
    return JsonResponse({'message': 'Pointage réinitialisé'}, status=status.HTTP_200_OK)


# #####################Créer une doléance######################
def create_doleance(request):
    print('create')
    if request.method == 'POST':
        form = DoleanceForm(request.POST)
        print("POST data:", request.POST)
        if form.is_valid():
            doleance = form.save(commit=False)
            doleance.element = form.cleaned_data['element']
            doleance.statut = "ATT"
            print("Form is valid")  # Debug print

            doleance = form.save()  # This should call the custom save method

            print("Doleance created:", doleance.__dict__)
            return redirect('gmao:home')
        else:
            print("Form errors:", form.errors)
    else:
        form = DoleanceForm()
    return render(request, 'gmao/create_doleance.html', {'form': form})


# #####################Récupérer la liste station ######################
def load_stations(request):
    client_id = request.GET.get('client')
    stations = Station.objects.filter(client_id=client_id).order_by('libelle_station')
    return JsonResponse(list(stations.values('id', 'libelle_station')), safe=False)


# #####################Récupérer la liste appelants ######################
# def load_appelants(request):
#     client_id = request.GET.get('client')
#     appelants = Appelant.objects.filter(client_id=client_id).order_by('nom_appelant')
#     return JsonResponse(list(appelants.values('ilogger.info(f"Dd', 'nom_appelant')), safe=False)
def load_appelants(request):
    client_id = request.GET.get('client')
    logger.info(f"Tentative de chargement des appelants pour le client_id: {client_id}")
    try:
        appelants = Appelant.objects.filter(client_id=client_id).order_by('nom_appelant')
        logger.info(f"Nombre d'appelants trouvés: {appelants.count()}")
        data = list(appelants.values('id', 'nom_appelant'))
        return JsonResponse(data, safe=False)
    except DatabaseError as e:
        logger.error(f"Erreur de base de données lors du chargement des appelants: {str(e)}")
        return JsonResponse({'error': 'Erreur de base de données'}, status=500)
    except Exception as e:
        logger.error(f"Erreur inattendue lors du chargement des appelants: {str(e)}")
        return JsonResponse({'error': 'Erreur serveur inattendue'}, status=500)


# #####################Récupérer la liste des éléments ######################

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

        if orientation not in ['R', 'L']:
            continue

        # Déterminer le numéro du pistolet en fonction de l'orientation et de la face de l'appareil
        if orientation == 'R':
            number = int(appareil.face_principal)
        else:  # 'L'
            number = int(appareil.face_secondaire)

        if appareil.num_serie and pistolet.produit and pistolet.produit.code_produit and pistolet.type_contrat:
            element = f"{number}-{appareil.num_serie}{orientation}-{pistolet.produit.code_produit}-{pistolet.type_contrat}"
            elements['Pistolets'].append((f"pistolet_{pistolet.id}", element))

    elements = {k: v for k, v in elements.items() if v}

    return JsonResponse(elements)


# #####################Commencer Travail ######################
def commencer_travail(request, intervention_id):
    intervention = get_object_or_404(Intervention, id=intervention_id)
    if not intervention.top_debut:
        intervention.top_debut = timezone.now()
        intervention.save()
    return redirect('gmao:detail_intervention', intervention_id=intervention.id)


# #####################Commencer interventions######################

@require_POST
def commencer_intervention(request, intervention_id):
    intervention = get_object_or_404(Intervention, id=intervention_id)
    if not intervention.top_debut:
        intervention.top_debut = timezone.now()
        intervention.save()

        # Mettre à jour le statut des techniciens à INT
        for intervention_personnel in intervention.interventionpersonnel_set.all():
            technicien = intervention_personnel.personnel
            technicien.statut = 'INT'
            technicien.save()

        return JsonResponse({'success': True, 'message': 'Intervention commencée'})
    return JsonResponse({'success': False, 'message': 'Intervention déjà commencée'})


@require_POST
def terminer_travail(request, intervention_id):
    intervention = get_object_or_404(Intervention, id=intervention_id)
    if not intervention.is_done:
        intervention.top_terminer = timezone.now()
        intervention.is_done = True
        intervention.is_half_done = False

        # Récupérer les données du formulaire
        intervention.description_panne = request.POST.get('description_panne')
        intervention.travaux_effectues = request.POST.get('travaux_effectues')
        intervention.observations = request.POST.get('observations')
        intervention.pieces_changees = request.POST.get('pieces_changees')
        statut_final = request.POST.get('statut_final')

        # Vérifier que statut_final n'est pas None
        if statut_final is None:
            return JsonResponse({'success': False, 'message': 'Le statut final est requis'})

        # Calcul de la durée d'intervention
        if intervention.top_debut:
            duree = intervention.top_terminer - intervention.top_debut
            intervention.duree_intervention = int(duree.total_seconds())

        intervention.save()

        # Mise à jour de la doléance
        doleance = intervention.doleance
        doleance.statut = statut_final  # Assurez-vous que cette ligne est présente
        if statut_final == 'TER':
            doleance.date_fin = intervention.top_terminer
        doleance.save()

        # Mise à jour du statut des techniciens
        for intervention_personnel in intervention.interventionpersonnel_set.all():
            technicien = intervention_personnel.personnel
            technicien.statut = 'PRS'
            technicien.save()

        return JsonResponse({'success': True, 'statut': statut_final})
    return JsonResponse({'success': False, 'message': 'Intervention déjà terminée'})


#
@require_GET
def get_techniciens_disponibles(request):
    techniciens = Personnel.objects.filter(statut='PRS')
    return JsonResponse({
        'success': True,
        'techniciens': list(techniciens.values('id', 'nom_personnel', 'prenom_personnel'))
    })


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
        is_half_done=True,
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


# def load_elements(request):
#     station_id = request.GET.get('station')
#     if not station_id:
#         return JsonResponse([], safe=False)
#
#     station = get_object_or_404(Station, id=station_id)
#     appareils = AppareilDistribution.objects.filter(piste__station_id=station_id)
#     pistolets = Pistolet.objects.filter(appareil_distribution__piste__station_id=station_id)
#
#     elements = {
#         'Appareil de distribution': [],
#         'Pistolets': [],
#         'Autres': [('lot_station', f'LOT STATION - {station.libelle_station}')]
#     }
#
#     for appareil in appareils:
#         if appareil.face_principal and appareil.face_secondaire and appareil.num_serie and appareil.type_contrat:
#             element = f"{appareil.face_principal}/{appareil.face_secondaire}-{appareil.num_serie}-{appareil.type_contrat}"
#             elements['Appareil de distribution'].append((f"appareil_{appareil.id}", element))
#
#     pistolet_count = {appareil.id: 0 for appareil in appareils}
#     for pistolet in pistolets:
#         appareil = pistolet.appareil_distribution
#         orientation = pistolet.orientation[0] if pistolet.orientation else ''
#
#         if orientation not in ['R', 'L']:
#             continue
#
#         pistolet_count[appareil.id] += 1
#         number = pistolet_count[appareil.id]
#         print('pistolet', pistolet)
#         print('number', number)
#
#         if appareil.num_serie and pistolet.produit and pistolet.produit.code_produit and pistolet.type_contrat:
#             element = f"{number}-{appareil.num_serie}{orientation}-{pistolet.produit.code_produit}-{pistolet.type_contrat}"
#             elements['Pistolets'].append(({pistolet.id}, element))
#
#     elements = {k: v for k, v in elements.items() if v}
#
#     return JsonResponse(elements)


# #####################Liste des interventions######################
def liste_interventions(request):
    interventions = (Intervention.objects.all()
                     .filter(top_depart__month=datetime.now().month)
                     .filter(top_depart__year=datetime.now().year)
                     .filter(top_depart__day=datetime.now().day)
                     .order_by('-top_depart'))
    return render(request, 'gmao/liste_interventions.html', {'interventions': interventions})


# #####################Détail d'une intervention######################
def detail_intervention(request, intervention_id):
    intervention = get_object_or_404(Intervention, id=intervention_id)
    techniciens = (InterventionPersonnel.objects.filter(intervention=intervention)
                   .all().select_related('personnel'))
    print("Techniciens associés:", [t.personnel.nom_personnel for t in techniciens])  # Ajoutez cette ligne
    return render(request, 'gmao/detail_intervention.html', {
        'intervention': intervention,
        'techniciens': techniciens
    })
